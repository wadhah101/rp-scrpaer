from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from typing import Any, cast

import click
from cloudpathlib import AnyPath, AzureBlobPath, CloudPath, GSPath, S3Path
from pydantic import BaseModel
from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096
yaml.indent(mapping=2, sequence=4, offset=2)


def _string_representer(representer: Any, data: str) -> Any:
    if data.isdigit():
        return representer.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return representer.represent_scalar("tag:yaml.org,2002:str", data)


yaml.representer.add_representer(str, _string_representer)


def _write_yaml(data: object, output_path: str) -> None:
    string_stream = io.StringIO()
    yaml.dump(data, string_stream)
    yaml_string = string_stream.getvalue()

    path: Path | CloudPath = AnyPath(output_path)  # type: ignore[assignment]
    if isinstance(path, Path):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml_string)
    click.echo(f"Wrote {path}")


def _serialize(obj: object) -> object:
    from datetime import datetime

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


def resolve_output_path(
    output: str | None, default_dir: str, export_type: str
) -> Path | CloudPath:
    if output is None:
        return cast(
            "Path | CloudPath",
            AnyPath(default_dir if export_type == "all" else f"{export_type}.json"),
        )
    return cast("Path | CloudPath", AnyPath(output))
