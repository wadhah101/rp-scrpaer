from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from uuid import UUID

import click
from api_service_rp.models.day import Day
from api_service_rp.models.mesocycle import Mesocycle
from hevy_api_service import ApiClient as HevyApiClient
from hevy_api_service import Configuration as HevyConfiguration
from hevy_api_service import WorkoutsApi
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
from ruamel.yaml import YAML

from rp_to_hevy_cli.hevy import _fetch_all_workouts

yaml = YAML()
yaml.width = 4096

DEFAULT_MATCHES_PATH = Path("data/embeddings/llm-matches.yaml")
DEFAULT_MESOCYCLES_PATH = Path("packages/cli/exports/rp/mesocycles.json")

IMPORT_TAG = "#import-from-rp"
RP_DAY_ID_PATTERN = re.compile(r"rp_day_id:(\d+)")


@dataclass
class ExerciseMatch:
    rp_id: str
    rp_name: str
    hevy_best_match_id: str
    hevy_best_match_name: str
    confidence: str


def _load_matches(path: Path) -> list[ExerciseMatch]:
    data = yaml.load(path)
    return [ExerciseMatch(**item) for item in data]


def _load_mesocycles(path: Path) -> list[Mesocycle]:
    raw = json.loads(path.read_text())
    return [Mesocycle.from_dict(m) for m in raw]


def _make_description(day_id: int) -> str:
    return f"{IMPORT_TAG}\nrp_day_id:{day_id}"


def _parse_existing_workout_dates(workouts: list) -> set[date]:
    """Extract the calendar date from each Hevy workout's start_time."""
    dates: set[date] = set()
    for w in workouts:
        st = getattr(w, "start_time", None)
        if isinstance(st, str):
            st = datetime.fromisoformat(st)
        if isinstance(st, datetime):
            dates.add(st.date())
    return dates


def _parse_imported_day_ids(workouts: list) -> set[int]:
    """Extract RP day IDs from Hevy workout descriptions."""
    ids: set[int] = set()
    for w in workouts:
        desc = getattr(w, "description", None) or ""
        match = RP_DAY_ID_PATTERN.search(desc)
        if match:
            ids.add(int(match.group(1)))
    return ids


def _is_day_importable(day: Day) -> bool:
    if not day.finished_at:
        return False
    if day.status in ("skipped", "ready"):
        return False
    for exercise in day.exercises:
        for s in exercise.sets:
            if s.status == "complete":
                return True
    return False


def _build_hevy_workout(
    day: Day,
    meso_name: str,
    week_index: int,
    matches: list[ExerciseMatch],
) -> HevyPostWorkoutsRequestBody | None:
    title = f"{meso_name} W{week_index + 1} - {day.label}"

    exercises: list[PostWorkoutsRequestExercise] = []
    earliest_finished_at: datetime | None = None

    for exercise in day.exercises:
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

        hevy_exercise = PostWorkoutsRequestExercise(
            exercise_template_id=exercise_match.hevy_best_match_id, sets=[]
        )

        for s in exercise.sets:
            if s.status == "skipped":
                continue
            if s.status == "complete":
                weight_kg = s.weight if s.unit == "kg" else s.weight * 0.453592
                hevy_set = PostWorkoutsRequestSet(
                    weight_kg=weight_kg, reps=s.reps, type="normal"
                )
                hevy_exercise.sets.append(hevy_set)

                if s.finished_at and (
                    earliest_finished_at is None or s.finished_at < earliest_finished_at
                ):
                    earliest_finished_at = s.finished_at

        if len(hevy_exercise.sets) > 0:
            exercises.append(hevy_exercise)

    if not exercises:
        return None

    start_time = (
        earliest_finished_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        if earliest_finished_at
        else day.finished_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    return HevyPostWorkoutsRequestBody(
        workout=PostWorkoutsRequestBodyWorkout(
            is_private=False,
            title=title,
            description=_make_description(day.id),
            start_time=start_time,
            end_time=day.finished_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            exercises=exercises,
        )
    )


@click.command("port-rp-workout-to-hevy")
@click.option(
    "--matches",
    "matches_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_MATCHES_PATH,
    help="Path to llm-matches.yaml file.",
)
@click.option(
    "--mesocycles",
    "mesocycles_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_MESOCYCLES_PATH,
    help="Path to mesocycles.json file.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Show what would be imported without posting.",
)
@click.option(
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="Only import days finished on or after this date (YYYY-MM-DD).",
)
def port_rp_workout_to_hevy(
    matches_path: Path,
    mesocycles_path: Path,
    dry_run: bool,
    start_date: datetime | None,
):
    asyncio.run(
        _port_rp_workout_to_hevy(matches_path, mesocycles_path, dry_run, start_date)
    )


async def _port_rp_workout_to_hevy(
    matches_path: Path,
    mesocycles_path: Path,
    dry_run: bool,
    start_date: datetime | None,
) -> None:
    """Port RP workout data to Hevy format."""

    # Phase 1: Load data
    matches = _load_matches(matches_path)
    mesocycles = _load_mesocycles(mesocycles_path)
    click.echo(f"Loaded {len(matches)} exercise matches")
    click.echo(f"Loaded {len(mesocycles)} mesocycles")

    # Phase 2: Validate
    api_key_str = os.environ.get("HEVY_API_KEY")
    if not api_key_str:
        raise click.ClickException(
            "HEVY_API_KEY environment variable is not set. "
            "Get your key at https://hevy.com/settings?developer"
        )
    api_key = UUID(api_key_str)

    # Phase 3: Fetch existing Hevy workouts for dedup
    config = HevyConfiguration(host=os.environ.get("HEVY_API_BASE_URL"))
    click.echo("Fetching existing Hevy workouts for dedup...")
    async with HevyApiClient(config) as client:
        workouts_api = WorkoutsApi(client)
        existing_workouts = await _fetch_all_workouts(workouts_api, api_key)

    existing_dates = _parse_existing_workout_dates(existing_workouts)
    imported_day_ids = _parse_imported_day_ids(existing_workouts)
    click.echo(
        f"Found {len(existing_dates)} workout dates "
        f"and {len(imported_day_ids)} RP day IDs in Hevy"
    )

    # Phase 4: Collect missing days
    to_import: list[tuple[HevyPostWorkoutsRequestBody, date, int]] = []
    stats = {
        "scanned": 0,
        "skipped_not_importable": 0,
        "skipped_before_start_date": 0,
        "skipped_already_imported": 0,
        "skipped_no_exercises": 0,
        "posted": 0,
        "failed": 0,
    }

    for meso in mesocycles:
        for week_idx, week in enumerate(meso.weeks):
            for day in week.days:
                stats["scanned"] += 1

                if not _is_day_importable(day):
                    stats["skipped_not_importable"] += 1
                    continue

                if start_date and day.finished_at.date() < start_date.date():
                    stats["skipped_before_start_date"] += 1
                    continue

                day_date = day.finished_at.date()
                if day_date in existing_dates or day.id in imported_day_ids:
                    stats["skipped_already_imported"] += 1
                    continue

                workout = _build_hevy_workout(day, meso.name, week_idx, matches)
                if workout is None:
                    stats["skipped_no_exercises"] += 1
                    continue

                to_import.append((workout, day_date, day.id))

    # Phase 5: Preview & confirm
    if not to_import:
        click.echo("Nothing to import — all RP days are already in Hevy or filtered.")
        _print_summary(stats)
        return

    click.echo(f"\n{len(to_import)} workout(s) to import:\n")
    click.echo(f"{'#':<4} {'Title':<45} {'Date':<20} {'Exercises':<10}")
    click.echo("-" * 79)
    for i, (workout, _wdate, _day_id) in enumerate(to_import, 1):
        w = workout.workout
        click.echo(f"{i:<4} {w.title:<45} {w.end_time:<20} {len(w.exercises):<10}")

    if dry_run:
        click.echo("\n--dry-run enabled, not posting.")
        _print_summary(stats)
        return

    if not click.confirm("\nProceed with import?"):
        click.echo("Aborted.")
        return

    # Phase 6: Post
    async with HevyApiClient(config) as client:
        workouts_api = WorkoutsApi(client)

        for workout, workout_date, day_id in to_import:
            try:
                result = await workouts_api.post_workouts(
                    api_key=api_key,
                    post_workouts_request_body=workout,
                )
                click.echo(
                    click.style(
                        f"  Created: {workout.workout.title} (hevy id: {result.id})",
                        fg="green",
                    )
                )
                stats["posted"] += 1
                existing_dates.add(workout_date)
                imported_day_ids.add(day_id)
            except Exception as e:
                click.echo(
                    click.style(
                        f"  FAILED: {workout.workout.title} — {e}",
                        fg="red",
                    )
                )
                stats["failed"] += 1

    # Phase 7: Summary
    _print_summary(stats)


def _print_summary(stats: dict[str, int]) -> None:
    click.echo("\n--- Summary ---")
    click.echo(f"  Scanned:                {stats['scanned']}")
    click.echo(f"  Skipped (not importable): {stats['skipped_not_importable']}")
    click.echo(f"  Skipped (before start):   {stats['skipped_before_start_date']}")
    click.echo(f"  Skipped (already in Hevy):{stats['skipped_already_imported']}")
    click.echo(f"  Skipped (no exercises):   {stats['skipped_no_exercises']}")
    click.echo(f"  Posted:                   {stats['posted']}")
    click.echo(f"  Failed:                   {stats['failed']}")
