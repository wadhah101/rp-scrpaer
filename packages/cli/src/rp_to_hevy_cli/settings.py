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


def require_hevy_api_key() -> UUID:
    return UUID(
        _require_env(
            "HEVY_API_KEY",
            "Get your key at https://hevy.com/settings?developer",
        )
    )


def require_rp_bearer_token() -> str:
    return _require_env(
        "RP_BEARER_TOKEN",
        "Get your bearer token from the RP Strength web app network traffic.",
    ).strip()


def rp_client(token: str) -> RpApiClient:
    return RpApiClient(RpConfiguration(access_token=token))


def hevy_client() -> HevyApiClient:
    return HevyApiClient(HevyConfiguration(host=os.environ.get("HEVY_API_BASE_URL")))
