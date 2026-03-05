from __future__ import annotations

import asyncio
import logging

from api_service_rp.models.mesocycle import Mesocycle
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from rp_to_hevy_cli.embedding.utils import RedisCache
from rp_to_hevy_cli.port.models import ExerciseMatch

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3

_SYSTEM_PROMPT = """\
You are an expert personal trainer. Given a list of exercises performed in a \
single workout session, generate a short (2-4 word) title that describes the \
session using standard gym naming conventions.

Examples of good titles: "Push Day", "Upper Body", "Chest & Triceps", \
"Back & Biceps", "Legs & Glutes", "Pull Day", "Shoulders & Arms", "Leg Day", \
"Full Body".

Rules:
- Return ONLY the title, nothing else.
- Keep it 2-4 words.
- Use "&" to join muscle groups when appropriate.
- Use common gym terminology."""


class WorkoutTitle(BaseModel):
    title: str


def build_title_agent(
    api_base_url: str,
    api_key: str,
    api_model: str,
) -> Agent[None, WorkoutTitle]:
    model = OpenAIChatModel(
        api_model,
        provider=OpenAIProvider(base_url=api_base_url, api_key=api_key),
    )
    return Agent(  # ty: ignore[invalid-return-type]
        model,
        system_prompt=_SYSTEM_PROMPT,
        output_type=WorkoutTitle,
    )


async def _generate_title_for_day(
    agent: Agent[None, WorkoutTitle],
    exercise_names: list[str],
    sem: asyncio.Semaphore,
    timeout: float,
    cache: RedisCache | None = None,
) -> str:
    user_prompt = "Exercises:\n" + "\n".join(f"- {name}" for name in exercise_names)

    # Deduplicate by sorting names for cache key
    cache_key = "Exercises:\n" + "\n".join(
        f"- {name}" for name in sorted(exercise_names)
    )

    if cache is not None:
        cached = await cache.get(cache_key)
        if cached is not None:
            print(f"Cache hit for {cache_key}")
            return WorkoutTitle.model_validate_json(cached).title

    async with sem:
        for attempt in range(_MAX_RETRIES):
            try:
                result = await asyncio.wait_for(agent.run(user_prompt), timeout=timeout)
                title = result.output.title
                break
            except TimeoutError:
                logger.warning(
                    "Timeout generating title (attempt %d/%d)",
                    attempt + 1,
                    _MAX_RETRIES,
                )
                if attempt < _MAX_RETRIES - 1:
                    continue
                return "Workout"
            except Exception as exc:
                logger.warning(
                    "Failed generating title (attempt %d/%d): %s",
                    attempt + 1,
                    _MAX_RETRIES,
                    exc,
                )
                if attempt < _MAX_RETRIES - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                return "Workout"
        else:
            return "Workout"

    if cache is not None:
        await cache.set(cache_key, result.output.model_dump_json())

    return title


async def generate_workout_titles(
    mesocycle: Mesocycle,
    matches: list[ExerciseMatch],
    agent: Agent[None, WorkoutTitle],
    sem: asyncio.Semaphore,
    timeout: float = 120.0,
    cache: RedisCache | None = None,
) -> Mesocycle:
    """Generate titles from the first week's exercises, then apply to all weeks."""
    meso = mesocycle.model_copy(deep=True)
    weeks = meso.weeks or []
    if not weeks:
        return meso

    match_map: dict[str, str] = {str(m.rp_id): m.hevy_best_match_name for m in matches}

    # Collect exercise names only from the first week.
    first_week = weeks[0]
    day_tasks: list[tuple[int, list[str]]] = []
    for day_idx, day in enumerate(first_week.days or []):
        exercise_names: list[str] = []
        for exercise in day.exercises or []:
            name = match_map.get(str(exercise.exercise_id))
            if name:
                exercise_names.append(name)
        if exercise_names:
            day_tasks.append((day_idx, exercise_names))

    if not day_tasks:
        return meso

    titles = await asyncio.gather(
        *(
            _generate_title_for_day(agent, names, sem, timeout, cache)
            for _, names in day_tasks
        )
    )

    # Apply generated titles to the matching day position across all weeks.
    title_by_day: dict[int, str] = {
        day_idx: title for (day_idx, _), title in zip(day_tasks, titles, strict=True)
    }
    for week in weeks:
        if week.days is None:
            continue
        for day_idx, day in enumerate(week.days):
            if day_idx in title_by_day:
                day.label = title_by_day[day_idx]

    return meso
