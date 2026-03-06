from __future__ import annotations

import asyncio

from api_service_rp.models.mesocycle import Mesocycle
from pydantic import BaseModel
from pydantic_ai import Agent

from rp_to_hevy_cli.port.models import ExerciseMatch
from rp_to_hevy_cli.utils import RedisCache, build_openai_agent, run_agent_cached

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
    return build_openai_agent(  # ty: ignore[invalid-return-type]
        api_base_url, api_key, api_model, _SYSTEM_PROMPT, WorkoutTitle
    )


async def _generate_title_for_day(
    agent: Agent[None, WorkoutTitle],
    exercise_names: list[str],
    sem: asyncio.Semaphore,
    timeout: float,
    cache: RedisCache | None = None,
) -> str:
    user_prompt = "Exercises:\n" + "\n".join(f"- {name}" for name in exercise_names)
    cache_key = "Exercises:\n" + "\n".join(
        f"- {name}" for name in sorted(exercise_names)
    )

    result = await run_agent_cached(
        agent,  # ty: ignore[invalid-argument-type]
        user_prompt,
        sem,
        timeout,
        cache=cache,
        cache_key=cache_key,
        output_type=WorkoutTitle,
    )
    if result is None:
        return "Workout"
    title: WorkoutTitle = result  # ty: ignore[invalid-assignment]
    return title.title


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
