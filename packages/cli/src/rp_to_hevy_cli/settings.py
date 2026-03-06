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


def hevy_client() -> tuple[HevyApiClient, UUID]:
    api_key = UUID(
        _require_env(
            "HEVY_API_KEY",
            "Get your key at https://hevy.com/settings?developer",
        )
    )
    client = HevyApiClient(HevyConfiguration(host=os.environ.get("HEVY_API_BASE_URL")))
    return client, api_key
