from __future__ import annotations

from datetime import date, datetime

import click

from rp_to_hevy_cli.port.models import RP_DAY_ID_PATTERN


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


def _parse_imported_day_ids(workouts: list) -> dict[int, str]:
    """Map RP day IDs to Hevy workout IDs from descriptions."""
    mapping: dict[int, str] = {}
    for w in workouts:
        desc = getattr(w, "description", None) or ""
        match = RP_DAY_ID_PATTERN.search(desc)
        if match:
            mapping[int(match.group(1))] = w.id
    return mapping


def _print_summary(stats: dict[str, int]) -> None:
    click.echo("\n--- Summary ---")
    click.echo(f"  Scanned:                {stats['scanned']}")
    click.echo(f"  Skipped (not importable): {stats['skipped_not_importable']}")
    click.echo(f"  Skipped (before start):   {stats['skipped_before_start_date']}")
    click.echo(f"  Skipped (already in Hevy):{stats['skipped_already_imported']}")
    click.echo(f"  Skipped (no exercises):   {stats['skipped_no_exercises']}")
    click.echo(f"  Created:                  {stats['created']}")
    click.echo(f"  Updated:                  {stats['updated']}")
    click.echo(f"  Failed:                   {stats['failed']}")
