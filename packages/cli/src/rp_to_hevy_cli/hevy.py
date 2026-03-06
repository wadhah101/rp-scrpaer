from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any
from uuid import UUID

import click
from cloudpathlib import CloudPath
from hevy_api_service import ExerciseTemplatesApi, WorkoutsApi

from rp_to_hevy_cli.settings import hevy_client
from rp_to_hevy_cli.utils import resolve_output_path, write_json

HEVY_EXPORT_TYPES = [
    "all",
    "exercise-templates",
    "workouts",
]


async def _fetch_all_pages[T](
    fetch: Callable[..., Awaitable[Any]],
    items_attr: str,
    api_key: UUID,
    page_size: int,
) -> list[T]:
    page = 1
    all_items: list[T] = []
    while True:
        resp = await fetch(api_key=api_key, page=page, page_size=page_size)
        items = getattr(resp, items_attr, None)
        if items:
            all_items.extend(items)
        if page >= (resp.page_count or 1):
            break
        page += 1
    return all_items


async def _hevy_export(export_type: str, output: Path | CloudPath) -> None:
    client, api_key = hevy_client()
    async with client:
        templates_api = ExerciseTemplatesApi(client)
        workouts_api = WorkoutsApi(client)

        if export_type != "all":
            fetchers = {
                "exercise-templates": lambda: _fetch_all_pages(
                    templates_api.get_exercise_templates,
                    "exercise_templates",
                    api_key,
                    100,
                ),
                "workouts": lambda: _fetch_all_pages(
                    workouts_api.get_workouts, "workouts", api_key, 10
                ),
            }
            write_json(await fetchers[export_type](), output)
            return

        templates, workouts = await asyncio.gather(
            _fetch_all_pages(
                templates_api.get_exercise_templates, "exercise_templates", api_key, 100
            ),
            _fetch_all_pages(workouts_api.get_workouts, "workouts", api_key, 10),
        )
        data = {"exercise_templates": templates, "workouts": workouts}
        if output.suffix == ".json":
            write_json(data, output)
        elif output.is_dir():
            if isinstance(output, Path):
                output.mkdir(parents=True, exist_ok=True)
            for key, value in data.items():
                write_json(value, output / f"{key}.json")
        else:
            raise click.ClickException(
                f"Invalid output path {output}. Must be .json or directory."
            )


@click.group()
def hevy():
    """Hevy app commands."""


@hevy.command("export")
@click.option(
    "--type",
    "export_type",
    type=click.Choice(HEVY_EXPORT_TYPES, case_sensitive=False),
    default="all",
    help="Type of data to export.",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output path. For 'all' without .json extension, exports to a directory.",
)
def hevy_export(export_type: str, output: str | None):
    """Export application data from Hevy to JSON."""
    output_path = resolve_output_path(output, "hevy-export", export_type)
    asyncio.run(_hevy_export(export_type, output_path))
