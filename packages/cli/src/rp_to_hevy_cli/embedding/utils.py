from __future__ import annotations

import atexit
import functools
import io
import os
import tempfile
from pathlib import Path

import click
from cloudpathlib import AnyPath, CloudPath
from embeddings import (
    ApiEmbedder,
    ClientMode,
    RateLimitConfig,
    create_client,
)
from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096
yaml.indent(mapping=2, sequence=4, offset=2)


# ---------------------------------------------------------------------------
# Shared option decorators
# ---------------------------------------------------------------------------


def _data_options(f):
    @click.option(
        "--rp-path",
        default="data/rp/exercises.json",
        help="Path to RP exercises JSON.",
    )
    @click.option(
        "--hevy-path",
        default="data/hevy/exercises.json",
        help="Path to Hevy exercises JSON.",
    )
    @click.option(
        "--mappings-path",
        default="data/muscle_group_mapping.json",
        help="Path to muscle-group mapping JSON.",
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def _embedder_options(f):
    @click.option("--api-base-url", required=True, help="API base URL.")
    @click.option("--api-key", required=True, help="API key.")
    @click.option("--api-model", required=True, help="API model name.")
    @click.option(
        "--api-dimensions", type=int, default=None, help="API embedding dimensions."
    )
    @click.option(
        "--api-max-rpm", type=int, default=60, help="API max requests per minute."
    )
    @click.option("--api-batch-size", type=int, default=100, help="API batch size.")
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def _chromadb_options(f):
    @click.option(
        "--chroma-mode",
        type=click.Choice(["memory", "persistent", "http"], case_sensitive=False),
        default="persistent",
        help="ChromaDB client mode.",
    )
    @click.option(
        "--chroma-path", default="./chroma_data", help="Path for persistent ChromaDB."
    )
    @click.option("--chroma-host", default="localhost", help="Host for HTTP ChromaDB.")
    @click.option(
        "--chroma-port", type=int, default=8000, help="Port for HTTP ChromaDB."
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def _common_options(f):
    f = _data_options(f)
    f = _embedder_options(f)
    f = _chromadb_options(f)
    return f


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_embedder(
    api_base_url: str,
    api_key: str,
    api_model: str,
    api_dimensions: int | None,
    api_max_rpm: int,
    api_batch_size: int,
) -> ApiEmbedder:
    return ApiEmbedder(
        base_url=api_base_url,
        api_key=api_key,
        model=api_model,
        dimensions=api_dimensions,
        rate_limit=RateLimitConfig(
            max_requests_per_minute=api_max_rpm,
            batch_size=api_batch_size,
        ),
    )


def _build_chroma_client(
    chroma_mode: str,
    chroma_path: str,
    chroma_host: str,
    chroma_port: int,
):
    return create_client(
        mode=ClientMode(chroma_mode),
        path=chroma_path,
        host=chroma_host,
        port=chroma_port,
    )


def _resolve_input(path_str: str) -> str:
    """If *path_str* is a cloud URI, download to a local temp file and return its path."""
    path = AnyPath(path_str)
    if isinstance(path, CloudPath):
        suffix = "".join(path.suffixes)
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(path.read_bytes())
        tmp.close()
        atexit.register(os.unlink, tmp.name)
        return tmp.name
    return path_str


def _write_yaml(data: object, output_path: str) -> None:

    path = AnyPath(output_path)
    string_stream = io.StringIO()
    yaml.dump(data, string_stream)
    yaml_string = string_stream.getvalue()

    if isinstance(path, CloudPath):
        path.write_text(yaml_string)
    else:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(yaml_string)
    click.echo(f"Wrote {path}")
