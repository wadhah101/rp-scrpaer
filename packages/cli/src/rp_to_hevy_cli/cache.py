from __future__ import annotations

import hashlib
import os

from sqlalchemy import Column, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.pool import StaticPool


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
