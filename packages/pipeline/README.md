# rp-to-hevy-pipeline

Kestra-based orchestration pipeline for automated workout data extraction, transformation, and export. This package handles the same data flow as the [CLI](../cli/README.md) but runs on a schedule with event-driven triggers, failure handling, retries, and user notifications.

**Status: in progress.** Flow definitions are in place with S3 triggers; task implementations are placeholders.

## Architecture

```
                ┌──────────────┐
                │  S3 Trigger  │  (file change on rp-to-hevy-data bucket)
                └──────┬───────┘
                       │
       ┌───────────────┼───────────────┐
       │                               │
  ┌────▼──────────────┐   ┌───────────▼───────────┐
  │  rp_to_hevy.api   │   │  rp_to_hevy.embeddings │
  │  Refresh exercises │   │  Exercise matching      │
  │  from RP + Hevy    │   │  on data change         │
  └────────────────────┘   └─────────────────────────┘
```

## Flows

| Flow | Namespace | Trigger | Description |
|------|-----------|---------|-------------|
| `refresh_rp_exercises_s3` | `rp_to_hevy.api` | — | Refresh exercises list from RP API |
| `refresh_hevy_exercises_s3` | `rp_to_hevy.api` | — | Refresh exercises list from Hevy API |
| `exercises_data_change_s3` | `rp_to_hevy.embeddings` | S3 `CREATE_OR_UPDATE` on `exports/exercises` | Run embeddings workflow on exercise data change |

## Local Development

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (for the Kestra server)
- [mise](https://mise.jdx.dev/) (installed at the repo root)

### Setup

1. Copy the environment template and fill in your credentials:

   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

2. Start the Kestra stack:

   ```bash
   mise //packages/pipeline:up
   ```

3. Open the Kestra UI at [http://localhost:8080](http://localhost:8080)

4. Flows are synced automatically from `flows/` via `micronaut.io.watch`.

### mise tasks

```bash
mise //packages/pipeline:up     # Start the Kestra stack
mise //packages/pipeline:down   # Stop the Kestra stack
mise //packages/pipeline:logs   # Tail Kestra container logs
```

## Configuration

Non-sensitive settings live in `application.yml` (tracked in git). Secrets (basic-auth credentials, AI keys) are injected via `KESTRA_CONFIGURATION` environment variable in `docker-compose.yaml`, sourced from `.env` (gitignored).

See `.env.example` for the required variables.

## Flow file naming

Flow files follow Kestra's local sync naming convention:

```
main_<namespace>.<flow_id>.yml
```

Where `main` is the tenant ID (always `main` in OSS Kestra), `<namespace>` uses dots for hierarchy, and `<flow_id>` is the flow identifier.
