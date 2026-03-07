from __future__ import annotations

import asyncio
from pathlib import Path

import click
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from rp_to_hevy_cli.cache import LLMCache
from rp_to_hevy_cli.embedding.judge_core import (
    _SYSTEM_PROMPT,
    JudgeResult,
    _Counter,
    _judge_one,
)
from rp_to_hevy_cli.settings import judge_llm_config
from rp_to_hevy_cli.utils import _write_yaml, yaml


async def _run(
    sample_size: int | None,
    input_dir: str,
    output: str,
    concurrency: int,
    timeout: float,
    strict: bool = False,
    cache_url: str = "sqlite+libsql:///data/cache.db",
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

    api_base_url, api_key, api_model = judge_llm_config()
    model = OpenAIChatModel(
        api_model, provider=OpenAIProvider(base_url=api_base_url, api_key=api_key)
    )
    agent = Agent(model, system_prompt=_SYSTEM_PROMPT, output_type=JudgeResult)
    sem = asyncio.Semaphore(concurrency)
    cache = LLMCache.from_url(cache_url, f"llm-judge:{api_model}")

    click.echo(
        f"Processing {total} exercises with {api_model} (concurrency={concurrency})..."
    )

    counter = _Counter(total)
    tasks = [
        _judge_one(agent, ex, sem, counter, timeout, strict, cache) for ex in exercises
    ]
    raw_results = await asyncio.gather(*tasks)
    click.echo(err=True)  # newline after progress

    cache.close()

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
    "--timeout",
    type=float,
    default=120.0,
    help="Per-request timeout in seconds.",
)
@click.option(
    "--strict",
    is_flag=True,
    default=False,
    help="Exit if LLM returns an out-of-range candidate number.",
)
@click.option(
    "--cache-url",
    default="sqlite+libsql:///data/cache.db",
    help="Cache database URL.",
)
def llm_judge(
    sample_size: int | None,
    concurrency: int,
    input_dir: str,
    output: str,
    timeout: float,
    strict: bool,
    cache_url: str,
) -> None:
    """Use an LLM to pick the best Hevy match for each RP exercise."""
    asyncio.run(
        _run(
            sample_size,
            input_dir,
            output,
            concurrency,
            timeout,
            strict,
            cache_url,
        )
    )
