from __future__ import annotations

import asyncio
import json
from pathlib import Path

import click
from api_service_rp import ApiClient, Configuration, TrainingDataApi, UserApi

EXPORT_TYPES = [
    "all",
    "profile",
    "subscriptions",
    "exercises",
    "mesocycles",
    "templates",
    "exercise-history",
]


def _read_token(token_file: str) -> str:
    path = Path(token_file)
    if not path.exists():
        raise click.ClickException(f"Token file not found: {token_file}")
    return path.read_text().strip()


def _serialize(obj: object) -> object:
    from datetime import datetime

    from pydantic import BaseModel

    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json", by_alias=True)
    if isinstance(obj, list):
        return [_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def _write_json(data: object, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(_serialize(data), indent=2, ensure_ascii=False))
    click.echo(f"Wrote {output}")


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
        *(training_api.get_mesocycle(m.key) for m in summaries)
    )
    return {
        "profile": profile,
        "subscriptions": subscriptions,
        "exercises": sorted(exercises, key=lambda e: e.id),
        "mesocycles": sorted(mesocycles, key=lambda m: m.created_at, reverse=True),
        "templates": sorted(templates, key=lambda t: t.id),
        "exercise_history": exercise_history,
    }


async def _fetch_mesocycles(training_api: TrainingDataApi) -> list:
    summaries = await training_api.get_mesocycles()
    return list(
        await asyncio.gather(*(training_api.get_mesocycle(m.key) for m in summaries))
    )


async def _export(token: str, export_type: str, output: Path) -> None:
    config = Configuration(access_token=token)
    async with ApiClient(config) as client:
        user_api = UserApi(client)
        training_api = TrainingDataApi(client)

        if export_type == "all":
            data = await _fetch_all(user_api, training_api)
            if output.suffix == ".json":
                _write_json(data, output)
            else:
                output.mkdir(parents=True, exist_ok=True)
                for key, value in data.items():
                    _write_json(value, output / f"{key}.json")
            return

        fetchers = {
            "profile": user_api.get_user_profile,
            "subscriptions": user_api.get_user_subscriptions,
            "exercises": training_api.get_exercises,
            "mesocycles": lambda: _fetch_mesocycles(training_api),
            "templates": training_api.get_templates,
            "exercise-history": training_api.get_user_exercise_history,
        }
        _write_json(await fetchers[export_type](), output)


@click.group()
def cli():
    """RP Hypertrophy to STRONG workout data exporter."""


@cli.command()
@click.option(
    "--token-file", default="token.txt", help="Path to file containing bearer token."
)
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
def export(token_file: str, export_type: str, output: str | None):
    """Export personal data from RP Hypertrophy to JSON."""
    token = _read_token(token_file)

    if output is None:
        output_path = (
            Path("export") if export_type == "all" else Path(f"{export_type}.json")
        )
    else:
        output_path = Path(output)

    asyncio.run(_export(token, export_type, output_path))


if __name__ == "__main__":
    cli()
