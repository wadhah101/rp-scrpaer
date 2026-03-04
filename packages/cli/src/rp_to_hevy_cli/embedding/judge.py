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


def _build_user_prompt(rp_name: str, candidates: list[str]) -> str:
    numbered = "\n".join(f"  {i}. {c}" for i, c in enumerate(candidates, 1))
    return f"RP Exercise: {rp_name}\n\nHevy Candidates:\n{numbered}"


def _resolve_hevy_id(name: str, matches: list[dict]) -> tuple[str | None, str]:
    """Map best_match name back to hevy_id and canonical name."""
    name_lower = name.lower().strip()
    for m in matches:
        candidate = m["hevy_embedding_name"]
        if candidate == name or candidate.lower().startswith(name_lower):
            return m["hevy_id"], candidate

    return None, name


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

    best_match = judge.best_match
    confidence = judge.confidence.value

    if best_match.lower() == "none":
        hevy_id = None
        hevy_name = "none"
    else:
        hevy_id, hevy_name = _resolve_hevy_id(best_match, matches)
        if hevy_id is None:
            msg = (
                f"rp_id={rp_id} — LLM returned "
                f"'{best_match}' which does not match "
                f"any candidate."
            )
            click.echo(
                click.style(
                    f"  ERROR: {msg}",
                    fg="red",
                    bold=True,
                ),
                err=True,
            )
            if strict:
                raise click.ClickException(msg)

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
    help="Exit on unresolved hevy_best_match_id.",
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
