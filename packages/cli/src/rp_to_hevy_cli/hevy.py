from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

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
    fetch: Callable[[int], Awaitable[Any]],
    items_attr: str,
) -> list[T]:
    first_resp = await fetch(1)
    page_count = first_resp.page_count or 1
    all_items: list[T] = list(getattr(first_resp, items_attr, None) or [])

    remaining = await asyncio.gather(*(fetch(p) for p in range(2, page_count + 1)))

    return all_items + [
        item for resp in remaining for item in (getattr(resp, items_attr, None) or [])
    ]


async def _hevy_export(export_type: str, output: Path | CloudPath) -> None:
    client, api_key = hevy_client()
    async with client:
        templates_api = ExerciseTemplatesApi(client)
        workouts_api = WorkoutsApi(client)

        fetchers = {
            "exercise-templates": lambda: _fetch_all_pages(
                lambda p: templates_api.get_exercise_templates(
                    api_key=api_key,
                    page=p,
                    page_size=100,
                ),
                "exercise_templates",
            ),
            "workouts": lambda: _fetch_all_pages(
                lambda p: workouts_api.get_workouts(
                    api_key=api_key,
                    page=p,
                    page_size=10,
                ),
                "workouts",
            ),
        }

        if export_type != "all":
            write_json(await fetchers[export_type](), output)
            return

        keys = list(fetchers)
        results = await asyncio.gather(*(f() for f in fetchers.values()))
        data = dict(zip(keys, results, strict=True))

        if output.suffix == ".json":
            write_json(data, output)
        elif output.suffix == "":
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
