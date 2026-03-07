from __future__ import annotations

import asyncio
import hashlib
import io
import json
import logging
import os
from pathlib import Path
from typing import Any, cast

import click
from cloudpathlib import AnyPath, AzureBlobPath, CloudPath, GSPath, S3Path
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ruamel.yaml import YAML
from sqlalchemy import Column, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# YAML
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# JSON I/O
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# LLM response cache (SQLAlchemy + libSQL)
# ---------------------------------------------------------------------------


class _Base(DeclarativeBase):
    pass


class _CacheEntry(_Base):
    __tablename__ = "cache_entries"
    namespace = Column(String(256), primary_key=True)
    field_hash = Column(String(64), primary_key=True)
    value = Column(Text(1024), nullable=False)


class LLMCache:
    """LLM response cache backed by SQLAlchemy + libSQL."""

    __slots__ = ("_engine", "_namespace")

    def __init__(self, engine, namespace: str) -> None:
        self._engine = engine
        self._namespace = namespace

    def get(self, prompt: str) -> str | None:
        fh = hashlib.sha256(prompt.encode()).hexdigest()
        with Session(self._engine) as session:
            row = session.get(_CacheEntry, (self._namespace, fh))
            return str(row.value) if row else None

    def set(self, prompt: str, value: str) -> None:
        from sqlalchemy.dialects.sqlite import insert

        fh = hashlib.sha256(prompt.encode()).hexdigest()
        with Session(self._engine) as session:
            stmt = (
                insert(_CacheEntry)
                .values(namespace=self._namespace, field_hash=fh, value=value)
                .on_conflict_do_update(
                    index_elements=["namespace", "field_hash"],
                    set_={"value": value},
                )
            )
            session.execute(stmt)
            session.commit()

    def close(self) -> None:
        self._engine.dispose()

    @classmethod
    def from_url(cls, db_url: str, namespace: str) -> LLMCache:
        connect_args: dict[str, str] = {}
        auth_token = os.environ.get("TURSO_AUTH_TOKEN")
        if auth_token:
            connect_args["auth_token"] = auth_token
        engine = create_engine(db_url, connect_args=connect_args, poolclass=StaticPool)
        _Base.metadata.create_all(engine)
        return cls(engine, namespace)


# ---------------------------------------------------------------------------
# LLM agent helpers
# ---------------------------------------------------------------------------


def build_openai_agent[T: BaseModel](
    api_base_url: str,
    api_key: str,
    api_model: str,
    system_prompt: str,
    output_type: type[T],
) -> Agent[None, T]:
    model = OpenAIChatModel(
        api_model,
        provider=OpenAIProvider(base_url=api_base_url, api_key=api_key),
    )
    return cast(
        "Agent[None, T]",
        Agent(model, system_prompt=system_prompt, output_type=output_type),
    )


async def run_agent_cached[T: BaseModel](
    agent: Agent[None, T],
    user_prompt: str,
    sem: asyncio.Semaphore,
    timeout: float,
    max_retries: int = 3,
    cache: LLMCache | None = None,
    cache_key: str | None = None,
    output_type: type[T] | None = None,
) -> T | None:
    """Run an agent with semaphore, retries, timeout, and optional cache."""
    key = cache_key or user_prompt

    if cache is not None and output_type is not None:
        cached_raw = cache.get(key)
        if cached_raw is not None:
            return output_type.model_validate_json(cached_raw)

    async with sem:
        for attempt in range(max_retries):
            try:
                result = await asyncio.wait_for(agent.run(user_prompt), timeout=timeout)
                output = result.output
                break
            except TimeoutError:
                logger.warning("Timeout (attempt %d/%d)", attempt + 1, max_retries)
                if attempt < max_retries - 1:
                    continue
                return None
            except Exception as exc:
                logger.warning(
                    "Failed (attempt %d/%d): %s", attempt + 1, max_retries, exc
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                return None
        else:
            return None

    if cache is not None:
        cache.set(key, output.model_dump_json())

    return output
