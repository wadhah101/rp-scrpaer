# rp-to-hevy-cli

Command-line tool for exporting workout data from the [RP Hypertrophy](https://rpstrength.com/) and [Hevy](https://www.hevyapp.com/) apps to JSON, plus semantic exercise matching via embeddings. Built with [Click](https://click.palletsprojects.com/) and powered by the workspace packages `api-service` and `embeddings`.

## Quick Start

```bash
# Run any command
mise //packages/cli:cli rp export
mise //packages/cli:cli hevy export
mise //packages/cli:cli embedding embd
```

## Command Groups

The CLI has three top-level groups:

### `rp` — RP Hypertrophy Export

Export personal workout data from the RP Hypertrophy app to JSON.

```
Usage: rp export [OPTIONS]

Options:
  --token-file TEXT   Path to bearer-token file  [default: token.txt]
  --type TEXT         Data type to export         [default: all]
  -o, --output PATH   Output file or directory
```

Grab your bearer token from the RP Strength web app and save it to `token.txt`.

| `--type` | Output | Description |
| --- | --- | --- |
| `all` *(default)* | `export/*.json` | Every data type below, one file each |
| `profile` | `profile.json` | User profile and attributes |
| `subscriptions` | `subscriptions.json` | Active subscriptions and purchase history |
| `exercises` | `exercises.json` | Full exercise catalog (~315 exercises) |
| `mesocycles` | `mesocycles.json` | All training blocks with weeks/days/exercises/sets |
| `templates` | `templates.json` | Built-in and custom training templates |
| `exercise-history` | `exercise_history.json` | Per-exercise last-performed timestamps |

### `hevy` — Hevy Export

Export exercise data from the Hevy app. Requires the `HEVY_API_KEY` environment variable (get it at https://hevy.com/settings?developer).

```
Usage: hevy export [OPTIONS]

Options:
  --type TEXT         Data type to export  [default: all]
  -o, --output PATH   Output file or directory
```

| `--type` | Description |
| --- | --- |
| `all` *(default)* | All data types to a directory |
| `exercise-templates` | Hevy exercise template catalog (~433 exercises) |

### `embedding` — Similarity Search

Embed RP and Hevy exercises into ChromaDB, then run similarity search to match RP exercises to their Hevy equivalents. See the [embeddings package](../embeddings/README.md) for background on the approach.

**`embedding embd`** — Encode exercises and store in ChromaDB:

```bash
mise //packages/cli:cli embedding embd \
  --backend local --model-name Qwen/Qwen3-Embedding-8B \
  --chroma-mode persistent --chroma-path ./chroma_data
```

**`embedding run-rp-similarity-search`** — Query already-embedded exercises:

```bash
mise //packages/cli:cli embedding run-rp-similarity-search \
  --chroma-mode persistent --chroma-path ./chroma_data \
  --metrics-output metrics.yaml --exercise-output-dir output/
```

Key options for both commands:
- `--backend` (`local` | `api`) — Use a local sentence-transformer or an OpenAI-compatible API
- `--model-name` — Model to load (default: `Qwen/Qwen3-Embedding-8B`)
- `--chroma-mode` (`memory` | `persistent` | `http`) — ChromaDB client mode
- `--rp-prompt` / `--hevy-prompt` — Instruction prompts prepended to exercise text

## Cloud Storage

All output paths (`-o` / `--output`) support cloud URIs via [cloudpathlib](https://cloudpathlib.drivendata.org/). Pass an S3, GCS, or Azure Blob path directly:

```bash
mise //packages/cli:cli rp export --all -o s3://my-bucket/exports/rp
mise //packages/cli:cli hevy export -o s3://my-bucket/exports/hevy/exercises.json
```

## mise Tasks

| Task | Description |
| --- | --- |
| `cli` | Run the CLI (`uv run python -m rp_to_hevy_cli`) |
| `export-rp-local` | Export all RP data to `exports/rp/` |
| `export-rp-s3` | Export all RP data to S3 (requires `BUCKET_NAME`) |
| `export-hevy-local` | Export Hevy exercises to `exports/hevy/` |
| `export-hevy-s3` | Export Hevy exercises to S3 (requires `BUCKET_NAME`) |
| `build` | Build the Docker image |

## Package Structure

```
src/rp_to_hevy_cli/
  __main__.py      # Click group: rp, hevy, embedding
  rp.py            # RP Hypertrophy export commands
  hevy.py          # Hevy export commands
  embedding.py     # Embedding + similarity search commands
  _utils.py        # Shared helpers (token reading, JSON serialization)
```

## Dependencies

| Package | Purpose |
| --- | --- |
| `click` >=8.1 | CLI framework |
| `pydantic` >=2.12 | Data validation |
| `api-service` | Async API clients for RP and Hevy (workspace) |
| `embeddings` | Embedding and similarity search library (workspace) |
| `cloudpathlib[s3]` | Cloud storage abstraction (S3, GCS, Azure) |
| `pyyaml` >=6.0 | YAML output for embedding results |

Requires **Python >= 3.12**.

## Docker

```bash
# Build only
mise //packages/cli:build

# Build + TruffleHog scan + push to registry
mise //packages/cli:build-push
```

3-stage build (mise → builder → `debian:trixie-slim` runtime):

- **BuildKit secret mounts** for `GITHUB_TOKEN` — never baked into image layers
- **`uv sync --frozen --compile-bytecode`** — reproducible installs with pre-compiled `.pyc` for fast startup
- **TruffleHog secret scan** gates every push — images are built locally (`--load`), scanned, then pushed only if clean
- **Pinned base image digest** (`debian:trixie-slim@sha256:...`) with pinned apt versions for deterministic builds
- **Non-root runtime** — runs as `app` user
- **Flat `/app/packages/` source copy** — all workspace `src/` dirs copied to a single directory with `PYTHONPATH` resolution

## Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `RP_APP_BASE_URL` | `https://training.rpstrength.com/api` | RP API base URL |
| `RP_APP_VERSION` | `1.1.13` | `accept-version` header value |
| `HEVY_API_KEY` | *(required)* | Hevy developer API key |
