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
determine which numbered candidate from the Hevy exercise database is the \
best match. The exercises may have different names but refer to the \
same or very similar movement.

Rules:
- You MUST pick exactly one candidate by its number.
- There is no "none" option — always pick the closest match.
- Return ONLY the candidate number (1, 2, 3, etc.)."""

_MAX_RETRIES = 3


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class JudgeResult(BaseModel):
    best_match: int
    confidence: Confidence


def _build_user_prompt(rp_name: str, candidates: list[str]) -> str:
    lines = "\n".join(f"  {i}. {c}" for i, c in enumerate(candidates, 1))
    return f"RP Exercise: {rp_name}\n\nHevy Candidates:\n{lines}"


async def _judge_one(
    agent: Agent[None, JudgeResult],
    exercise: dict,
    sem: asyncio.Semaphore,
    strict: bool = False,
) -> dict | None:
    """Judge a single exercise with retries."""
    rp_id = str(exercise["rp_id"])
    rp_name = exercise["rp_embedding_name"]
    matches = exercise["semantic_matches"]
    candidates = [m["hevy_embedding_name"] for m in matches]
    user_prompt = _build_user_prompt(rp_name, candidates)

    async with sem:
        for attempt in range(_MAX_RETRIES):
            try:
                result = await agent.run(user_prompt)
                judge = result.output
                break
            except Exception as exc:
                if attempt < _MAX_RETRIES - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                logger.warning(
                    "Failed for rp_id=%s, skipping: %s",
                    rp_id,
                    exc,
                )
                return None
        else:
            return None

    idx = judge.best_match - 1  # 1-based → 0-based
    if idx < 0 or idx >= len(matches):
        click.echo(
            click.style(
                f"  OUT OF RANGE: rp_id={rp_id} — LLM returned "
                f"{judge.best_match} but only {len(matches)} candidates. "
                f"Falling back to candidate 1.",
                fg="red",
                bold=True,
            ),
            err=True,
        )
        if strict:
            raise click.ClickException(
                f"rp_id={rp_id} — LLM returned {judge.best_match} "
                f"which is out of range (1-{len(matches)})."
            )
        idx = 0

    chosen = matches[idx]
    return {
        "rp_id": rp_id,
        "rp_name": rp_name,
        "hevy_best_match_id": chosen["hevy_id"],
        "hevy_best_match_name": chosen["hevy_embedding_name"],
        "confidence": judge.confidence.value,
    }


async def _run(
    api_base_url: str,
    api_key: str,
    api_model: str,
    sample_size: int | None,
    input_dir: str,
    output: str,
    concurrency: int,
    strict: bool = False,
) -> None:
    input_path = Path(input_dir)
    files = sorted(input_path.glob("*.yaml"))
    if not files:
        raise click.ClickException(f"No YAML files found in {input_dir}")

    if sample_size is not None:
        click.echo(
            f"Warning: --sample-size={sample_size}, results will be incomplete.",
            err=True,
        )
        files = files[:sample_size]

    exercises = [yaml.load(f.read_text()) for f in files]
    total = len(exercises)

    model = OpenAIChatModel(
        api_model,
        provider=OpenAIProvider(base_url=api_base_url, api_key=api_key),
    )
    agent = Agent(
        model,
        system_prompt=_SYSTEM_PROMPT,
        output_type=JudgeResult,
    )
    sem = asyncio.Semaphore(concurrency)

    click.echo(
        f"Processing {total} exercises with {api_model} (concurrency={concurrency})..."
    )

    tasks = [_judge_one(agent, ex, sem, strict) for ex in exercises]
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
@click.option(
    "--strict",
    is_flag=True,
    default=False,
    help="Exit if LLM returns an out-of-range candidate number.",
)
def llm_judge(
    api_base_url: str,
    api_key: str,
    api_model: str,
    sample_size: int | None,
    concurrency: int,
    input_dir: str,
    output: str,
    strict: bool,
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
            strict,
        )
    )
