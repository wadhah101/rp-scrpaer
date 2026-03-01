# rp-to-strong-pipeline

Dagster-based orchestration pipeline for automated workout data extraction, transformation, and export. This package handles the same data flow as the [CLI](../cli/README.md) but runs on a schedule with DAG-based execution, failure handling, retries, and user notifications.

**Status: scaffolded, not yet implemented.** The package structure and Dockerfile are in place; assets and resources are placeholders.

## Planned Architecture

```
                ┌──────────────┐
                │   Scheduler  │  (cron / sensor)
                └──────┬───────┘
                       │
          ┌────────────▼────────────┐
          │  Extract RP + Hevy Data │  (assets)
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │   Transform with Polars │  (assets)
          └────────────┬────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
  ┌────▼────┐   ┌──────▼──────┐  ┌────▼────┐
  │  Export  │   │  Embedding  │  │  Notify │
  │      │   │  Matching   │  │  User   │
  │  CSV     │   │  (optional) │  │         │
  └─────────┘   └─────────────┘  └─────────┘
```

### Responsibilities

- **Scheduled extraction** --- Pull workout data from RP and Hevy APIs on a cron schedule (or triggered by a sensor)
- **DAG execution** --- Dagster manages the dependency graph so steps run in the right order with proper retries on failure
- **Failure handling** --- Built-in retry policies and alerting when API calls or transformations fail
- **User communication** --- Notify users on successful exports or when manual intervention is needed (e.g., expired tokens)

### Differences from the CLI

| | CLI | Pipeline |
|---|---|---|
| Trigger | Manual (user runs a command) | Scheduled (cron) or event-driven (sensor) |
| Failure handling | Exits with error code | Retries with backoff, sends alerts |
| User input | Token file, CLI flags | Dagster UI / config, stored credentials |
| Orchestration | Single async function | Dagster DAG with observable assets |
| Monitoring | Terminal output | Dagster webserver dashboard |

## Package Structure

```
src/rp_to_strong_pipeline/
  __init__.py
  assets/           # Dagster software-defined assets (placeholder)
    __init__.py
  resources/        # Dagster resources — API clients, config (placeholder)
    __init__.py
```

## Dependencies

| Package | Purpose |
|---|---|
| `dagster` >=1.9 | Orchestration framework |
| `dagster-webserver` >=1.9 | Web UI for monitoring and triggering runs |
| `polars` >=1.0 | Data transformation |
| `httpx` >=0.27 | Async HTTP client |

Requires **Python >= 3.12**.

## Docker

```bash
mise //packages/pipeline:build
```

Multi-stage build (debian:trixie-slim runtime). Runs `dagster-webserver` on port 3000 as non-root `app` user.
