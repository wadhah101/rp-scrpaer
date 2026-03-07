from __future__ import annotations

import os
from uuid import UUID

import click
from api_service_rp import ApiClient as RpApiClient
from api_service_rp import Configuration as RpConfiguration
from hevy_api_service import ApiClient as HevyApiClient
from hevy_api_service import Configuration as HevyConfiguration


def _require_env(name: str, hint: str) -> str:
    raw = os.environ.get(name)
    if not raw:
        raise click.ClickException(f"{name} is not set. {hint}")
    return raw


def rp_client() -> RpApiClient:
    token = _require_env(
        "RP_BEARER_TOKEN",
        "Get your bearer token from the RP Strength web app network traffic.",
    ).strip()
    return RpApiClient(
        RpConfiguration(
            host=os.environ.get("RP_APP_BASE_URL"),
            access_token=token,
        )
    )


def title_llm_config() -> tuple[str, str, str]:
    base_url = _require_env("TITLE_API_BASE_URL", "Set the LLM API base URL.")
    api_key = _require_env("TITLE_API_KEY", "Set the LLM API key.")
    model = _require_env("TITLE_API_MODEL", "Set the LLM model name.")
    return base_url, api_key, model


def embedding_api_config() -> tuple[str, str, str, int | None, int]:
    base_url = _require_env(
        "EMBEDDING_API_BASE_URL", "Set the embedding API base URL."
    )
    api_key = _require_env("EMBEDDING_API_KEY", "Set the embedding API key.")
    model = _require_env("EMBEDDING_API_MODEL", "Set the embedding model name.")
    dimensions = os.environ.get("EMBEDDING_API_DIMENSIONS")
    batch_size = int(os.environ.get("EMBEDDING_API_BATCH_SIZE", "100"))
    return (
        base_url,
        api_key,
        model,
        int(dimensions) if dimensions else None,
        batch_size,
    )


def judge_llm_config() -> tuple[str, str, str]:
    base_url = _require_env("JUDGE_API_BASE_URL", "Set the judge LLM API base URL.")
    api_key = _require_env("JUDGE_API_KEY", "Set the judge LLM API key.")
    model = _require_env("JUDGE_API_MODEL", "Set the judge LLM model name.")
    return base_url, api_key, model


def chroma_config() -> tuple[str, int, str | None]:
    host = os.environ.get("CHROMA_HOST", "localhost")
    port = int(os.environ.get("CHROMA_PORT", "8000"))
    api_key = os.environ.get("CHROMA_API_KEY")
    return host, port, api_key


def hevy_client() -> tuple[HevyApiClient, UUID]:
    api_key = UUID(
        _require_env(
            "HEVY_API_KEY",
            "Get your key at https://hevy.com/settings?developer",
        )
    )
    client = HevyApiClient(HevyConfiguration(host=os.environ.get("HEVY_API_BASE_URL")))
    return client, api_key
