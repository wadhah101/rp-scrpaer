from __future__ import annotations

import asyncio
import logging
import sys
from enum import Enum

import click
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from rp_to_hevy_cli.embedding.utils import RedisCache

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are an expert in resistance training and exercise science.

Given an exercise from the RP (Renaissance Periodization) database, \
determine which numbered candidate from the Hevy exercise database is the \
best match. The exercises may have different names but refer to the \
same or very similar movement.

Rules:
- You MUST pick exactly one candidate by its number.
- There is no "none" option — always pick the closest match.
- Don't justify your choice for me
- Return ONLY the candidate number (1, 2, 3, etc.)."""

_MAX_RETRIES = 10


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


class _Counter:
    __slots__ = ("_done", "_total", "_cached")

    def __init__(self, total: int) -> None:
        self._done = 0
        self._cached = 0
        self._total = total

    def tick(self, *, cached: bool = False) -> None:
        self._done += 1
        if cached:
            self._cached += 1
        sys.stderr.write(f"\r  {self._done}/{self._total}")
        sys.stderr.flush()


def _resolve_match(
    judge: JudgeResult,
    exercise: dict,
    strict: bool,
) -> dict:
    rp_id = str(exercise["rp_id"])
    matches = exercise["semantic_matches"]
    idx = judge.best_match - 1
    if idx < 0 or idx >= len(matches):
        if strict:
            raise click.ClickException(
                f"rp_id={rp_id} — best_match {judge.best_match} "
                f"is out of range (1-{len(matches)})."
            )
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
        idx = 0
    chosen = matches[idx]
    return {
        "rp_id": rp_id,
        "rp_name": exercise["rp_embedding_name"],
        "hevy_best_match_id": chosen["hevy_id"],
        "hevy_best_match_name": chosen["hevy_embedding_name"],
    }


def build_agent(
    api_base_url: str,
    api_key: str,
    api_model: str,
) -> Agent[None, JudgeResult]:
    model = OpenAIChatModel(
        api_model,
        provider=OpenAIProvider(base_url=api_base_url, api_key=api_key),
    )
    return Agent(  # ty: ignore[invalid-return-type]
        model,
        system_prompt=_SYSTEM_PROMPT,
        output_type=JudgeResult,
    )


async def _judge_one(
    agent: Agent[None, JudgeResult],
    exercise: dict,
    sem: asyncio.Semaphore,
    counter: _Counter,
    timeout: float,
    strict: bool = False,
    cache: RedisCache | None = None,
) -> dict | None:
    """Judge a single exercise with retries."""
    rp_id = str(exercise["rp_id"])
    candidates = [m["hevy_embedding_name"] for m in exercise["semantic_matches"]]
    user_prompt = _build_user_prompt(exercise["rp_embedding_name"], candidates)

    # Check cache before acquiring semaphore / calling LLM
    if cache is not None:
        cached = await cache.get(user_prompt)
        if cached is not None:
            judge = JudgeResult.model_validate_json(cached)
            counter.tick(cached=True)
            return _resolve_match(judge, exercise, strict)

    async with sem:
        for attempt in range(_MAX_RETRIES):
            try:
                result = await asyncio.wait_for(agent.run(user_prompt), timeout=timeout)
                judge = result.output
                break
            except TimeoutError:
                logger.warning(
                    "Timeout for rp_id=%s (attempt %d/%d)",
                    rp_id,
                    attempt + 1,
                    _MAX_RETRIES,
                )
                if attempt < _MAX_RETRIES - 1:
                    continue
                return None
            except Exception as exc:
                click.echo(
                    click.style(f"FAILED for reason {exc}", fg="red", bold=True),
                    err=True,
                )
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

    # Cache the result
    if cache is not None:
        await cache.set(user_prompt, judge.model_dump_json())

    counter.tick()
    return _resolve_match(judge, exercise, strict)
