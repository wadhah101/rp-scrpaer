from __future__ import annotations

import json
from pathlib import Path

import click


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
