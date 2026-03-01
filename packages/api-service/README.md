# api-service

Generated async Python SDK clients for the [Hevy](https://api.hevyapp.com/docs/) and [RP Strength](https://training.rpstrength.com/api) APIs, produced from their OpenAPI specs using `openapi-generator-cli`.

## Generated packages

Two independent packages live under `src/`:

| Package | Source spec | APIs |
|---------|------------|------|
| `hevy_api_service` | `openapi/hevy.openapi.yaml` | Workouts, Routines, Routine Folders, Exercise Templates, Exercise History, Users |
| `api_service_rp` | `openapi/rp.openapi.yaml` | Auth, Training, Training Data, User, Purchases, App |

Both use the `asyncio` library backend (`aiohttp`).

## How the specs are produced

- **Hevy** — The spec is scraped and fixed by [`scripts/hevy-extract`](../../scripts/hevy-extract/). The `generate-libs-hevy` task depends on it automatically.
- **RP** — The spec at `openapi/rp.openapi.yaml` is hand-authored.

## Prerequisites

Managed by [mise](https://mise.jdx.dev/) (see `.mise.toml`):

- Java 21 (for openapi-generator)
- Node + `@openapitools/openapi-generator-cli` 2.30.0 (generator CLI v7.20.0)
- `@redocly/cli` 2.20.0 (for building HTML docs)
- Bun (for the hevy-extract dependency)
- Python >= 3.12

## Code generation

```sh
# Generate the Hevy SDK (also fetches + fixes the spec via hevy-extract)
mise run generate-libs-hevy

# Generate the RP SDK
mise run generate-libs-rp
```

Both commands run `openapi-generator-cli generate` with `-g python`, `--package-name <name>`, and `library=asyncio`.

## API docs

Build and serve static Redocly HTML docs:

```sh
# Hevy
mise run compile-openai-hevy
mise run serve-openapi-hevy

# RP
mise run compile-openai-rp
mise run serve-openapi-rp
```

## Docker

The Dockerfile builds the Redocly HTML docs and serves them with Caddy on port 8080.

## Environment variables

Set in `.mise.toml` for code generation and local development:

| Variable | Default |
|----------|---------|
| `HEVY_API_BASE_URL` | `https://api.hevyapp.com` |
| `RP_APP_BASE_URL` | `https://training.rpstrength.com/api` |
| `RP_APP_VERSION` | `1.1.13` |

## Usage

```python
from hevy_api_service import WorkoutsApi, ApiClient, Configuration

config = Configuration(host="https://api.hevyapp.com")
async with ApiClient(config) as client:
    api = WorkoutsApi(client)
    response = await api.get_workouts(api_key="...")
```

```python
from api_service_rp import TrainingApi, ApiClient, Configuration

config = Configuration(host="https://training.rpstrength.com/api")
async with ApiClient(config) as client:
    api = TrainingApi(client)
    response = await api.get_mesocycles(...)
```

## Tasks summary

| Task | Description |
|------|-------------|
| `generate-libs-hevy` | Fetch Hevy spec + generate Python SDK |
| `generate-libs-rp` | Generate RP Python SDK |
| `compile-openai-hevy` | Build Hevy Redocly HTML docs |
| `serve-openapi-hevy` | Serve Hevy docs locally |
| `compile-openai-rp` | Build RP Redocly HTML docs |
| `serve-openapi-rp` | Serve RP docs locally |
