from __future__ import annotations

import asyncio
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any
from uuid import UUID

import click
from cloudpathlib import AnyPath, CloudPath
from hevy_api_service import ApiClient as HevyApiClient
from hevy_api_service import Configuration as HevyConfiguration
from hevy_api_service import ExerciseTemplatesApi, WorkoutsApi

from rp_to_hevy_cli.utils import _require_hevy_api_key, write_json

HEVY_EXPORT_TYPES = [
    "all",
    "exercise-templates",
    "workouts",
]


def _hevy_client() -> HevyApiClient:
    config = HevyConfiguration(host=os.environ.get("HEVY_API_BASE_URL"))
    return HevyApiClient(config)


async def _fetch_all_pages(
    fetch: Callable[..., Awaitable[Any]],
    items_attr: str,
    api_key: UUID,
    page_size: int,
) -> list:
    page = 1
    all_items: list = []
    while True:
        resp = await fetch(api_key=api_key, page=page, page_size=page_size)
        items = getattr(resp, items_attr, None)
        if items:
            all_items.extend(items)
        if page >= (resp.page_count or 1):
            break
        page += 1
    return all_items


async def _fetch_all_exercise_templates(
    templates_api: ExerciseTemplatesApi, api_key: UUID
) -> list:
    return await _fetch_all_pages(
        templates_api.get_exercise_templates, "exercise_templates", api_key, 100
    )


async def _fetch_all_workouts(workouts_api: WorkoutsApi, api_key: UUID) -> list:
    return await _fetch_all_pages(workouts_api.get_workouts, "workouts", api_key, 10)


async def _hevy_export(
    api_key: UUID, export_type: str, output: Path | CloudPath
) -> None:
    async with _hevy_client() as client:
        templates_api = ExerciseTemplatesApi(client)
        workouts_api = WorkoutsApi(client)

        if export_type == "exercise-templates":
            data = await _fetch_all_exercise_templates(templates_api, api_key)
            write_json(data, output)
            return

        if export_type == "workouts":
            data = await _fetch_all_workouts(workouts_api, api_key)
            write_json(data, output)
            return

        # all
        templates, workouts = await asyncio.gather(
            _fetch_all_exercise_templates(templates_api, api_key),
            _fetch_all_workouts(workouts_api, api_key),
        )
        data = {
            "exercise_templates": templates,
            "workouts": workouts,
        }
        if output.suffix == ".json":
            write_json(data, output)
        else:
            if isinstance(output, Path):
                output.mkdir(parents=True, exist_ok=True)
            for name, value in data.items():
                write_json(value, output / f"{name}.json")


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
    api_key = _require_hevy_api_key()

    if output is None:
        output_path = AnyPath(
            "hevy-export" if export_type == "all" else f"{export_type}.json"
        )
    else:
        output_path = AnyPath(output)

    asyncio.run(_hevy_export(api_key, export_type, output_path))
