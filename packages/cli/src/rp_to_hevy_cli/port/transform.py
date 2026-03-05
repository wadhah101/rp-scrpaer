from __future__ import annotations

from datetime import datetime, timedelta

import click
from api_service_rp.models.day import Day
from hevy_api_service.models import (
    PostWorkoutsRequestBody as HevyPostWorkoutsRequestBody,
)
from hevy_api_service.models.post_workouts_request_body_workout import (
    PostWorkoutsRequestBodyWorkout,
)
from hevy_api_service.models.post_workouts_request_exercise import (
    PostWorkoutsRequestExercise,
)
from hevy_api_service.models.post_workouts_request_set import PostWorkoutsRequestSet

from rp_to_hevy_cli.port.models import IMPORT_TAG, ExerciseMatch

MIN_DURATION = timedelta(minutes=45)
MAX_DURATION = timedelta(hours=2)


def _make_description(day_id: int) -> str:
    return f"{IMPORT_TAG}\nrp-day-id:{day_id}"


def _is_day_importable(day: Day) -> bool:
    if not day.finished_at:
        return False
    if day.status in ("skipped", "ready"):
        return False
    for exercise in day.exercises or []:
        for s in exercise.sets or []:
            if s.status == "complete":
                return True
    return False


def _build_hevy_workout(
    day: Day,
    meso_name: str,
    week_index: int,
    matches: list[ExerciseMatch],
) -> HevyPostWorkoutsRequestBody | None:
    title = day.label or f"{meso_name} W{week_index + 1}"

    exercises: list[PostWorkoutsRequestExercise] = []
    earliest_finished_at: datetime | None = None

    for exercise in day.exercises or []:
        exercise_match = next(
            (m for m in matches if str(m.rp_id) == str(exercise.exercise_id)), None
        )

        if exercise_match is None:
            click.echo(
                click.style(
                    f"  WARNING: No match for exercise_id "
                    f"{exercise.exercise_id}, skipping",
                    fg="yellow",
                )
            )
            continue

        hevy_sets: list[PostWorkoutsRequestSet] = []

        for s in exercise.sets or []:
            if s.status == "skipped":
                continue
            if s.status == "complete" and s.weight is not None:
                weight_kg = s.weight if s.unit == "kg" else s.weight * 0.453592
                hevy_sets.append(
                    PostWorkoutsRequestSet(
                        weight_kg=weight_kg, reps=s.reps, type="normal"
                    )
                )

                if s.finished_at and (
                    earliest_finished_at is None or s.finished_at < earliest_finished_at
                ):
                    earliest_finished_at = s.finished_at

        if hevy_sets:
            exercises.append(
                PostWorkoutsRequestExercise(
                    exercise_template_id=exercise_match.hevy_best_match_id,
                    sets=hevy_sets,
                )
            )

    if not exercises:
        return None

    assert day.finished_at is not None
    assert day.id is not None
    start = earliest_finished_at or day.finished_at
    duration = day.finished_at - start
    clamped = max(MIN_DURATION, min(MAX_DURATION, duration))
    end = start + clamped

    return HevyPostWorkoutsRequestBody(
        workout=PostWorkoutsRequestBodyWorkout(
            is_private=False,
            title=title,
            description=_make_description(day.id),
            start_time=start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time=end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            exercises=exercises,
        )
    )
