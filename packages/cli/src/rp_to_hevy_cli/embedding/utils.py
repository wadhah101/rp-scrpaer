from __future__ import annotations

import atexit
import functools
import os
import tempfile

import click
from cloudpathlib import AnyPath, CloudPath


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
    @click.option("--chroma-host", default="localhost", help="ChromaDB server host.")
    @click.option(
        "--chroma-port", type=int, default=8000, help="ChromaDB server port."
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


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
