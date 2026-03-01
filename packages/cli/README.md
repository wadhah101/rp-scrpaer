# rp-to-strong-cli

Command-line tool for exporting personal workout data from the [RP Hypertrophy](https://rpstrength.com/) app to JSON. Built with [Click](https://click.palletsprojects.com/) and powered by the `rp-to-strong-api-service-rp` library.

## Quick Start

1. Grab your bearer token from the RP Strength web app and save it to `token.txt`.
2. Run the export:

```bash
mise run cli              # or: mise run cli export
```

This creates an `export/` directory with one JSON file per data type.

## CLI Reference

```
Usage: main.py export [OPTIONS]

Options:
  --token-file TEXT  Path to bearer-token file  [default: token.txt]
  --type TEXT        Data type to export         [default: all]
  -o, --output PATH  Output file or directory
```

### Export types

| `--type` | Output | Description |
| --- | --- | --- |
| `all` *(default)* | `export/*.json` | Every data type below, one file each |
| `profile` | `profile.json` | User profile and attributes |
| `subscriptions` | `subscriptions.json` | Active subscriptions and purchase history |
| `exercises` | `exercises.json` | Full exercise catalog (~315 exercises) |
| `mesocycles` | `mesocycles.json` | All training blocks with weeks/days/exercises/sets |
| `templates` | `templates.json` | Built-in and custom training templates |
| `exercise-history` | `exercise_history.json` | Per-exercise last-performed timestamps |

### Examples

```bash
# Export everything to export/
mise run cli export

# Export only mesocycles to a custom path
mise run cli export --type mesocycles -o data/mesocycles.json

# Use a different token file
mise run cli export --token-file ~/.config/rp/token.txt
```

## Package Structure

```
src/rp_to_strong_cli/
  __init__.py
  main.py      # Click CLI — reads token, calls RPClient, writes JSON
swagger.yaml   # OpenAPI 3.0.3 spec for the RP Strength API
export/        # Default output directory (sample data included)
```

## Dependencies

| Package | Purpose |
| --- | --- |
| `click` >=8.1 | CLI framework |
| `rp-to-strong-api-service-rp` | Async API client and Pydantic models |
| `aiohttp` >=3.13 | Async HTTP (transitive) |
| `aiofiles` >=25.1 | Async file I/O |
| `pydantic` >=2.12 | Data validation (transitive) |

Requires **Python >= 3.12**.

## Docker

```bash
mise run build       # builds multi-stage image (debian:trixie-slim runtime)
```

The image uses a non-root `app` user and defaults to a `bash` entrypoint.

## Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `RP_APP_BASE_URL` | `https://training.rpstrength.com/api` | API base URL |
| `RP_APP_VERSION` | `1.1.13` | `accept-version` header value |
