from __future__ import annotations

import asyncio
import enum
import sys

import click
from pydantic import BaseModel
from pydantic_ai import Agent

from rp_to_hevy_cli.agent import run_agent_cached
from rp_to_hevy_cli.cache import LLMCache

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


class Confidence(enum.StrEnum):
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
    __slots__ = ("_done", "_total")

    def __init__(self, total: int) -> None:
        self._done = 0
        self._total = total

    def tick(self) -> None:
        self._done += 1
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


async def _judge_one(
    agent: Agent[None, JudgeResult],
    exercise: dict,
    sem: asyncio.Semaphore,
    counter: _Counter,
    timeout: float,
    strict: bool = False,
    cache: LLMCache | None = None,
) -> dict | None:
    """Judge a single exercise with retries."""
    candidates = [m["hevy_embedding_name"] for m in exercise["semantic_matches"]]
    user_prompt = _build_user_prompt(exercise["rp_embedding_name"], candidates)

    judge = await run_agent_cached(
        agent,
        user_prompt,
        sem,
        timeout,
        max_retries=_MAX_RETRIES,
        cache=cache,
        output_type=JudgeResult,
    )
    if judge is None:
        return None

    counter.tick()
    return _resolve_match(judge, exercise, strict)
