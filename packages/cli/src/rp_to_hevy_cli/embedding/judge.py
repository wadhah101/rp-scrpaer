from __future__ import annotations

import asyncio
from pathlib import Path

import click
from ruamel.yaml import YAML

from rp_to_hevy_cli.embedding.judge_core import _Counter, _judge_one, build_agent
from rp_to_hevy_cli.embedding.utils import RedisCache, _write_yaml

yaml = YAML()
yaml.width = 4096


async def _run(
    api_base_url: str,
    api_key: str,
    api_model: str,
    sample_size: int | None,
    input_dir: str,
    output: str,
    concurrency: int,
    timeout: float,
    strict: bool = False,
    redis_url: str | None = None,
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

    agent = build_agent(api_base_url, api_key, api_model)
    sem = asyncio.Semaphore(concurrency)

    cache: RedisCache | None = None
    if redis_url is not None:
        cache = RedisCache.from_url(redis_url, f"llm-judge:{api_model}")

    click.echo(
        f"Processing {total} exercises with {api_model} (concurrency={concurrency})..."
    )

    counter = _Counter(total)
    tasks = [
        _judge_one(agent, ex, sem, counter, timeout, strict, cache) for ex in exercises
    ]
    raw_results = await asyncio.gather(*tasks)
    click.echo(err=True)  # newline after progress

    if cache is not None:
        await cache.close()

    results = [r for r in raw_results if r is not None]
    results.sort(key=lambda r: int(r["rp_id"]))

    _write_yaml(results, output)
    skipped = total - len(results)
    msg = f"Done. {len(results)}/{total} exercises matched."
    if counter._cached:
        msg += f" ({counter._cached} cached, {len(results) - counter._cached} via LLM)"
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
    "--redis-url",
    default=None,
    help="Redis URL for caching LLM results, e.g. redis://127.0.0.1:6379",
)
def llm_judge(
    api_base_url: str,
    api_key: str,
    api_model: str,
    sample_size: int | None,
    concurrency: int,
    input_dir: str,
    output: str,
    timeout: float,
    strict: bool,
    redis_url: str | None,
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
            timeout,
            strict,
            redis_url,
        )
    )
