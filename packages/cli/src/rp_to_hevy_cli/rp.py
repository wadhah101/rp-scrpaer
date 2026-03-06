from __future__ import annotations

import asyncio
from pathlib import Path

import click
from api_service_rp import TrainingDataApi, UserApi
from api_service_rp.models.mesocycle import Mesocycle
from cloudpathlib import CloudPath

from rp_to_hevy_cli.settings import rp_client
from rp_to_hevy_cli.utils import resolve_output_path, write_json

EXPORT_TYPES = [
    "all",
    "profile",
    "subscriptions",
    "exercises",
    "mesocycles",
    "templates",
    "exercise-history",
]


async def _fetch_all(user_api: UserApi, training_api: TrainingDataApi) -> dict:
    (
        profile,
        subscriptions,
        exercises,
        summaries,
        templates,
        exercise_history,
    ) = await asyncio.gather(
        user_api.get_user_profile(),
        user_api.get_user_subscriptions(),
        training_api.get_exercises(),
        training_api.get_mesocycles(),
        training_api.get_templates(),
        training_api.get_user_exercise_history(),
    )
    mesocycles = await asyncio.gather(
        *(training_api.get_mesocycle(m.key) for m in summaries if m.key)
    )
    return {
        "profile": profile,
        "subscriptions": subscriptions,
        "exercises": sorted(exercises, key=lambda e: e.id),
        "mesocycles": sorted(mesocycles, key=lambda m: m.created_at, reverse=True),
        "templates": sorted(templates, key=lambda t: t.id),
        "exercise_history": exercise_history,
    }


async def _fetch_mesocycles(training_api: TrainingDataApi) -> list[Mesocycle]:
    summaries = await training_api.get_mesocycles()
    return list(
        await asyncio.gather(
            *(training_api.get_mesocycle(m.key) for m in summaries if m.key)
        )
    )


async def _export(export_type: str, output: Path | CloudPath) -> None:
    async with rp_client() as client:
        user_api = UserApi(client)
        training_api = TrainingDataApi(client)

        if export_type == "all":
            data = await _fetch_all(user_api, training_api)
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
            return

        fetchers = {
            "profile": user_api.get_user_profile,
            "subscriptions": user_api.get_user_subscriptions,
            "exercises": training_api.get_exercises,
            "mesocycles": lambda: _fetch_mesocycles(training_api),
            "templates": training_api.get_templates,
            "exercise-history": training_api.get_user_exercise_history,
        }
        write_json(await fetchers[export_type](), output)


@click.group()
def rp():
    """RP Hypertrophy commands."""


@rp.command()
@click.option(
    "--type",
    "export_type",
    type=click.Choice(EXPORT_TYPES, case_sensitive=False),
    default="all",
    help="Type of data to export.",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output path. For 'all' without .json extension, exports to a directory with one file per type.",
)
def export(export_type: str, output: str | None):
    """Export personal data from RP Hypertrophy to JSON."""
    output_path = resolve_output_path(output, "export", export_type)
    asyncio.run(_export(export_type, output_path))
