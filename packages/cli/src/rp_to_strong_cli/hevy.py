from __future__ import annotations

import asyncio
import os
from pathlib import Path
from uuid import UUID

import click
from hevy_api_service import ApiClient as HevyApiClient
from hevy_api_service import Configuration as HevyConfiguration
from hevy_api_service import ExerciseTemplatesApi

from ._utils import _write_json

HEVY_EXPORT_TYPES = [
    "all",
    "exercise-templates",
]


async def _fetch_all_exercise_templates(
    templates_api: ExerciseTemplatesApi, api_key: UUID
) -> list:
    page = 1
    all_templates = []
    while True:
        resp = await templates_api.get_exercise_templates(
            api_key=api_key, page=page, page_size=100
        )
        if resp.exercise_templates:
            all_templates.extend(resp.exercise_templates)
        if page >= (resp.page_count or 1):
            break
        page += 1
    return all_templates


async def _hevy_export(api_key: str, export_type: str, output: Path) -> None:
    key = UUID(api_key)
    config = HevyConfiguration(host="https://api.hevyapp.com")
    async with HevyApiClient(config) as client:
        templates_api = ExerciseTemplatesApi(client)

        if export_type == "exercise-templates":
            data = await _fetch_all_exercise_templates(templates_api, key)
            _write_json(data, output)
            return

        # all
        data = {
            "exercise_templates": await _fetch_all_exercise_templates(
                templates_api, key
            ),
        }
        if output.suffix == ".json":
            _write_json(data, output)
        else:
            output.mkdir(parents=True, exist_ok=True)
            for name, value in data.items():
                _write_json(value, output / f"{name}.json")


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
    api_key = os.environ.get("HEVY_API_KEY")
    if not api_key:
        raise click.ClickException(
            "HEVY_API_KEY environment variable is not set. "
            "Get your key at https://hevy.com/settings?developer"
        )

    if output is None:
        output_path = (
            Path("hevy-export") if export_type == "all" else Path(f"{export_type}.json")
        )
    else:
        output_path = Path(output)

    asyncio.run(_hevy_export(api_key, export_type, output_path))
