from __future__ import annotations

import asyncio
from datetime import date, datetime
from pathlib import Path
from typing import cast

import click
from api_service_rp import TrainingDataApi
from api_service_rp.models.mesocycle import Mesocycle
from hevy_api_service import GetWorkouts200Response, WorkoutsApi
from hevy_api_service.models import (
    PostWorkoutsRequestBody as HevyPostWorkoutsRequestBody,
)
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from rp_to_hevy_cli.cache import LLMCache
from rp_to_hevy_cli.hevy import _fetch_all_pages
from rp_to_hevy_cli.port.models import DEFAULT_MATCHES_PATH, _load_matches
from rp_to_hevy_cli.port.sync import (
    _parse_existing_workout_dates,
    _parse_imported_day_ids,
    _print_summary,
)
from rp_to_hevy_cli.port.transform import _build_hevy_workout, _is_day_importable
from rp_to_hevy_cli.port.workout_title_generator import (
    _SYSTEM_PROMPT as _TITLE_SYSTEM_PROMPT,
)
from rp_to_hevy_cli.port.workout_title_generator import (
    WorkoutTitle,
    generate_workout_titles,
)
from rp_to_hevy_cli.rp import _fetch_mesocycles
from rp_to_hevy_cli.settings import hevy_client, rp_client, title_llm_config


@click.command("port-rp-workout-to-hevy")
@click.option(
    "--matches",
    "matches_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_MATCHES_PATH,
    help="Path to llm-matches.yaml file.",
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
@click.option(
    "--upsert",
    is_flag=True,
    default=False,
    help="Update existing imported workouts instead of skipping them.",
)
@click.option(
    "--title-concurrency",
    type=int,
    default=10,
    help="Max concurrent title-generation requests.",
)
@click.option(
    "--title-timeout",
    type=float,
    default=120.0,
    help="Per-request timeout for title generation (seconds).",
)
@click.option(
    "--cache-url",
    default="sqlite+libsql:///data/cache.db",
    help="Cache database URL.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip confirmation prompt.",
)
def port_rp_workout_to_hevy(
    matches_path: Path,
    dry_run: bool,
    start_date: datetime | None,
    upsert: bool,
    title_concurrency: int,
    title_timeout: float,
    cache_url: str,
    yes: bool,
):
    asyncio.run(
        _port_rp_workout_to_hevy(
            matches_path=matches_path,
            dry_run=dry_run,
            start_date=start_date,
            upsert=upsert,
            title_concurrency=title_concurrency,
            title_timeout=title_timeout,
            cache_url=cache_url,
            yes=yes,
        )
    )


async def _port_rp_workout_to_hevy(
    matches_path: Path,
    dry_run: bool,
    start_date: datetime | None,
    upsert: bool = False,
    title_concurrency: int = 10,
    title_timeout: float = 120.0,
    cache_url: str = "sqlite+libsql:///data/cache.db",
    yes: bool = False,
) -> None:
    """Port RP workout data to Hevy format."""

    # Phase 1: Load matches + fetch mesocycles from RP
    matches = _load_matches(matches_path)
    click.echo(f"Loaded {len(matches)} exercise matches")

    click.echo("Fetching mesocycles from RP...")
    async with rp_client() as client:
        mesocycles: list[Mesocycle] = await _fetch_mesocycles(TrainingDataApi(client))
    click.echo(f"Fetched {len(mesocycles)} mesocycles")

    # Phase 2: Fetch existing Hevy workouts for dedup
    click.echo("Fetching existing Hevy workouts for dedup...")
    hevy, api_key = hevy_client()
    async with hevy:
        workouts_api = WorkoutsApi(hevy)
        existing_workouts: list[GetWorkouts200Response] = await _fetch_all_pages(
            lambda p: workouts_api.get_workouts(
                api_key=api_key,
                page=p,
                page_size=10,
            ),
            "workouts",
        )

    existing_dates = _parse_existing_workout_dates(existing_workouts)
    imported_day_ids = _parse_imported_day_ids(existing_workouts)
    click.echo(
        f"Found {len(existing_dates)} workout dates "
        f"and {len(imported_day_ids)} RP day IDs in Hevy"
    )

    # Phase 4: Collect days to create/update
    # Each entry: (workout_body, day_date, day_id, hevy_workout_id | None)
    to_import: list[tuple[HevyPostWorkoutsRequestBody, date, int, str | None]] = []
    stats = {
        "scanned": 0,
        "skipped_not_importable": 0,
        "skipped_before_start_date": 0,
        "skipped_already_imported": 0,
        "skipped_no_exercises": 0,
        "created": 0,
        "updated": 0,
        "failed": 0,
    }

    title_api_base_url, title_api_key, title_api_model = title_llm_config()
    click.echo(f"Generating workout titles via {title_api_model}...")
    title_model = OpenAIChatModel(
        title_api_model,
        provider=OpenAIProvider(base_url=title_api_base_url, api_key=title_api_key),
    )
    title_agent = cast(
        Agent[None, WorkoutTitle],
        Agent(
            title_model,
            system_prompt=_TITLE_SYSTEM_PROMPT,
            output_type=WorkoutTitle,
        ),
    )
    sem = asyncio.Semaphore(title_concurrency)

    cache = LLMCache.from_url(cache_url, f"workout-titles:{title_api_model}")

    titled_mesos: list[Mesocycle] = await asyncio.gather(
        *(
            generate_workout_titles(m, matches, title_agent, sem, title_timeout, cache)
            for m in mesocycles
        )
    )

    cache.close()

    for meso in titled_mesos:
        for week_idx, week in enumerate(meso.weeks or []):
            for day in week.days or []:
                stats["scanned"] += 1

                if not _is_day_importable(day):
                    stats["skipped_not_importable"] += 1
                    continue

                if start_date and day.finished_at.date() < start_date.date():
                    stats["skipped_before_start_date"] += 1
                    continue

                day_date = day.finished_at.date()
                hevy_id = imported_day_ids.get(day.id)

                if hevy_id and upsert:
                    pass  # will update below
                elif day_date in existing_dates or hevy_id:
                    stats["skipped_already_imported"] += 1
                    continue

                workout = _build_hevy_workout(day, meso.name or "", week_idx, matches)
                if workout is None:
                    stats["skipped_no_exercises"] += 1
                    continue

                to_import.append((workout, day_date, day.id, hevy_id))

    # Phase 5: Preview & confirm
    if not to_import:
        click.echo("Nothing to import — all RP days are already in Hevy or filtered.")
        _print_summary(stats)
        return

    n_create = sum(1 for *_, hid in to_import if hid is None)
    n_update = sum(1 for *_, hid in to_import if hid is not None)
    click.echo(f"\n{len(to_import)} workout(s) ({n_create} new, {n_update} update):\n")
    header = (
        f"{'#':<4} {'Action':<8} {'Title':<35} {'Date':<12} {'Duration':<10} {'Ex':>3}"
    )
    click.echo(header)
    click.echo("-" * len(header))
    for i, (workout, _, _, hevy_id) in enumerate(to_import, 1):
        w = workout.workout
        action = "UPDATE" if hevy_id else "CREATE"
        start = datetime.fromisoformat(w.start_time)
        end = datetime.fromisoformat(w.end_time)
        mins = int((end - start).total_seconds() // 60)
        duration = f"{mins // 60}h{mins % 60:02d}m"
        click.echo(
            f"{i:<4} {action:<8} {w.title:<35} "
            f"{end.strftime('%Y-%m-%d'):<12} "
            f"{duration:<10} {len(w.exercises):>3}"
        )

    if dry_run:
        click.echo("\n--dry-run enabled, not posting.")
        _print_summary(stats)
        return

    if not yes and not click.confirm("\nProceed with import?"):
        click.echo("Aborted.")
        return

    # Phase 6: Post / Put
    hevy, api_key = hevy_client()
    async with hevy:
        workouts_api = WorkoutsApi(hevy)

        for workout, workout_date, day_id, hevy_id in to_import:
            assert workout.workout is not None
            try:
                if hevy_id:
                    await workouts_api.put_workouts_workout_id(
                        api_key=api_key,
                        workout_id=hevy_id,
                        post_workouts_request_body=workout,
                    )
                    click.echo(
                        click.style(
                            f"  Updated: {workout.workout.title}",
                            fg="cyan",
                        )
                    )
                    stats["updated"] += 1
                else:
                    result = await workouts_api.post_workouts(
                        api_key=api_key,
                        post_workouts_request_body=workout,
                    )
                    click.echo(
                        click.style(
                            f"  Created: {workout.workout.title} "
                            f"(hevy id: {result.id})",
                            fg="green",
                        )
                    )
                    stats["created"] += 1
                existing_dates.add(workout_date)
                imported_day_ids[day_id] = hevy_id or ""
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
