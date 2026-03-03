from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import click
from cloudpathlib import AnyPath, AzureBlobPath, CloudPath, GSPath, S3Path


def read_token(token_file: str) -> str:
    path = AnyPath(token_file)
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


def write_json(data: object, output: Path | CloudPath) -> None:
    data_to_write = json.dumps(_serialize(data), indent=2, ensure_ascii=False).encode(
        "utf-8"
    )

    if isinstance(output, Path):
        output.parent.mkdir(parents=True, exist_ok=True)

    elif output.exists() and isinstance(output, (S3Path, AzureBlobPath, GSPath)):
        memory_file = io.BytesIO()
        memory_file.write(data_to_write)
        memory_file.seek(0)
        md5_hash = hashlib.md5()
        md5_hash.update(memory_file.read())
        hex_digest = md5_hash.hexdigest()
        remote_file_md5 = output.etag.strip('"')

        if str(remote_file_md5) == hex_digest:
            click.echo(f"Skipping {output} (MD5 hash matches)")
            return

    output.write_bytes(data_to_write)
    click.echo(f"Wrote {output}")
