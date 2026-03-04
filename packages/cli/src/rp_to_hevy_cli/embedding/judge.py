from __future__ import annotations

import asyncio
import logging
from enum import Enum
from pathlib import Path

import click
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ruamel.yaml import YAML

from rp_to_hevy_cli.embedding.utils import _write_yaml

logger = logging.getLogger(__name__)

yaml = YAML()
yaml.width = 4096

_SYSTEM_PROMPT = """\
You are an expert in resistance training and exercise science.

Given an exercise from the RP (Renaissance Periodization) database, \
determine which candidate from the Hevy exercise database is the \
best match. The exercises may have different names but refer to the \
same or very similar movement.

Rules:
- Pick the single best match from the candidates.
- If NONE of the candidates are a reasonable match, set \
best_match to "none"."""

_MAX_RETRIES = 3


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class JudgeResult(BaseModel):
    best_match: str
    confidence: Confidence


class _AdaptiveRateLimiter:
    """Async token-bucket rate limiter that backs off on 429s."""

    _MIN_INTERVAL = 0.01  # 6000 RPM ceiling

    def __init__(self, initial_rpm: int = 1000) -> None:
        self._interval = 60.0 / initial_rpm
        self._lock = asyncio.Lock()
        self._next_allowed: float = 0.0

    @property
    def current_rpm(self) -> int:
        return int(60.0 / self._interval)

    async def acquire(self) -> None:
        async with self._lock:
            loop = asyncio.get_event_loop()
            now = loop.time()
            if now < self._next_allowed:
                await asyncio.sleep(self._next_allowed - now)
            self._next_allowed = loop.time() + self._interval

    def on_success(self) -> None:
        self._interval = max(
            self._interval * 0.95, self._MIN_INTERVAL
        )

    async def on_rate_limit(
        self, retry_after: float | None
    ) -> None:
        async with self._lock:
            self._interval *= 1.5
            pause = max(
                retry_after
                if retry_after and retry_after > 0
                else 0,
                self._interval,
            )
            click.echo(
                f"  Rate limited, sleeping {pause:.1f}s "
                f"(~{self.current_rpm} RPM)",
                err=True,
            )
            await asyncio.sleep(pause)
            loop = asyncio.get_event_loop()
            self._next_allowed = loop.time() + self._interval


def _build_user_prompt(
    rp_name: str, candidates: list[str]
) -> str:
    numbered = "\n".join(
        f"  {i}. {c}" for i, c in enumerate(candidates, 1)
    )
    return (
        f"RP Exercise: {rp_name}\n\n"
        f"Hevy Candidates:\n{numbered}"
    )


def _resolve_hevy_id(
    name: str, matches: list[dict]
) -> str | None:
    """Map best_match name back to hevy_id from candidates."""
    for m in matches:
        if m["hevy_embedding_name"] == name:
            return m["hevy_id"]
    return None


def _is_rate_limit(exc: Exception) -> tuple[bool, float | None]:
    """Check if exception is a 429 and extract retry-after."""
    from openai import RateLimitError

    if isinstance(exc, RateLimitError):
        retry = None
        if (
            hasattr(exc, "response")
            and exc.response is not None
        ):
            val = exc.response.headers.get("retry-after")
            if val:
                retry = float(val)
        return True, retry
    if hasattr(exc, "__cause__") and isinstance(
        exc.__cause__, RateLimitError
    ):
        return _is_rate_limit(exc.__cause__)
    return False, None


async def _judge_one(
    agent: Agent[None, JudgeResult],
    limiter: _AdaptiveRateLimiter,
    exercise: dict,
    sem: asyncio.Semaphore,
) -> dict | None:
    """Judge a single exercise with retries and rate limiting."""
    rp_id = str(exercise["rp_id"])
    rp_name = exercise["rp_embedding_name"]
    matches = exercise["semantic_matches"]
    candidates = [m["hevy_embedding_name"] for m in matches]
    user_prompt = _build_user_prompt(rp_name, candidates)

    async with sem:
        for attempt in range(_MAX_RETRIES):
            await limiter.acquire()
            try:
                result = await agent.run(user_prompt)
                limiter.on_success()
                judge = result.output
                break
            except Exception as exc:
                is_429, retry_after = _is_rate_limit(exc)
                if is_429:
                    await limiter.on_rate_limit(retry_after)
                    continue
                if attempt < _MAX_RETRIES - 1:
                    continue
                logger.warning(
                    "Failed for rp_id=%s, skipping: %s",
                    rp_id,
                    exc,
                )
                return None
        else:
            logger.warning(
                "Exhausted retries for rp_id=%s", rp_id
            )
            return None

    best_match = judge.best_match
    confidence = judge.confidence.value

    if best_match.lower() == "none":
        hevy_id = None
        hevy_name = "none"
    else:
        hevy_id = _resolve_hevy_id(best_match, matches)
        hevy_name = best_match

    return {
        "rp_id": rp_id,
        "rp_name": rp_name,
        "hevy_best_match_id": hevy_id,
        "hevy_best_match_name": hevy_name,
        "confidence": confidence,
    }


async def _run(
    api_base_url: str,
    api_key: str,
    api_model: str,
    sample_size: int | None,
    input_dir: str,
    output: str,
    concurrency: int,
) -> None:
    input_path = Path(input_dir)
    files = sorted(input_path.glob("*.yaml"))
    if not files:
        raise click.ClickException(
            f"No YAML files found in {input_dir}"
        )

    if sample_size is not None:
        click.echo(
            f"Warning: --sample-size={sample_size}, "
            "results will be incomplete.",
            err=True,
        )
        files = files[:sample_size]

    exercises = [yaml.load(f.read_text()) for f in files]
    total = len(exercises)

    model = OpenAIChatModel(
        api_model,
        provider=OpenAIProvider(
            base_url=api_base_url, api_key=api_key
        ),
    )
    agent = Agent(
        model,
        system_prompt=_SYSTEM_PROMPT,
        output_type=JudgeResult,
    )

    limiter = _AdaptiveRateLimiter()
    sem = asyncio.Semaphore(concurrency)

    click.echo(
        f"Processing {total} exercises with {api_model} "
        f"(concurrency={concurrency})..."
    )

    tasks = [
        _judge_one(agent, limiter, ex, sem)
        for ex in exercises
    ]
    raw_results = await asyncio.gather(*tasks)

    results = [r for r in raw_results if r is not None]
    results.sort(key=lambda r: int(r["rp_id"]))

    _write_yaml(results, output)
    skipped = total - len(results)
    msg = f"Done. {len(results)}/{total} exercises matched."
    if skipped:
        msg += f" ({skipped} skipped)"
    click.echo(msg)


@click.command("llm-judge")
@click.option(
    "--api-base-url",
    required=True,
    help="OpenAI-compatible API base URL.",
)
@click.option("--api-key", required=True, help="API key.")
@click.option("--api-model", required=True, help="Model name.")
@click.option(
    "--sample-size",
    type=int,
    default=None,
    help="Only process first N exercises.",
)
@click.option(
    "--concurrency",
    type=int,
    default=50,
    help="Max concurrent requests.",
)
@click.option(
    "--input-dir",
    default="data/embeddings/output",
    help="Directory of per-exercise YAML files.",
)
@click.option(
    "--output",
    default="data/embeddings/llm-matches.yaml",
    help="Combined YAML output path.",
)
def llm_judge(
    api_base_url: str,
    api_key: str,
    api_model: str,
    sample_size: int | None,
    concurrency: int,
    input_dir: str,
    output: str,
) -> None:
    """Use an LLM to pick the best Hevy match for each RP exercise."""
    asyncio.run(
        _run(
            api_base_url,
            api_key,
            api_model,
            sample_size,
            input_dir,
            output,
            concurrency,
        )
    )
