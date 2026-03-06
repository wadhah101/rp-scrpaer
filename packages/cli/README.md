# rp-to-hevy-cli

Command-line tool for porting workout history from [RP Hypertrophy](https://rpstrength.com/) to [Hevy](https://www.hevyapp.com/). Exports data from both platforms, matches exercises via semantic embeddings, and imports complete training blocks into Hevy. Built with [Click](https://click.palletsprojects.com/) and powered by the workspace packages `api-service` and `embeddings`.

## Quick Start

```bash
# Run any command
mise //packages/cli:cli rp export
mise //packages/cli:cli hevy export
mise //packages/cli:cli embedding embd
```

## Command Groups

The CLI has three top-level groups plus a standalone command:

### `rp` — RP Hypertrophy Export

Export personal workout data from RP Hypertrophy's reverse-engineered internal API to JSON. The API has no public documentation — endpoints were discovered by inspecting the mobile app's network traffic.

```
Usage: rp export [OPTIONS]

Options:
  --type TEXT         Data type to export         [default: all]
  -o, --output PATH   Output file or directory
```

Set `RP_BEARER_TOKEN` to your bearer token from the RP Strength web app network traffic.

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

### `embedding` — AI-Powered Exercise Matching

RP and Hevy have completely different exercise catalogs (~315 vs ~433 exercises) with different naming conventions, so we use a multi-stage AI pipeline to match them:

1. **Embed** — Each exercise is turned into a rich text representation (name + equipment + muscle groups) and encoded into a vector using [Qwen3-Embedding-8B](https://huggingface.co/Qwen/Qwen3-Embedding-8B) (FP16), a local sentence-transformer model. Vectors are stored in ChromaDB for fast retrieval.
2. **Search** — For every RP exercise, we query the Hevy collection by cosine similarity and retrieve the top-K nearest candidates.
3. **Judge** — An LLM (`gemini-3.1-pro-preview` via OpenRouter) reviews each RP exercise and its top-K candidates, then picks the single best match. Results are written to [`data/embeddings/llm-matches.yaml`](../../data/embeddings/llm-matches.yaml) — a flat list mapping every RP exercise ID/name to a Hevy exercise ID/name with a confidence rating (`high`, `medium`, or `low`).

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

**`embedding llm-judge`** — LLM picks the best match from candidates:

```bash
mise //packages/cli:cli embedding llm-judge \
  --api-base-url https://openrouter.ai/api/v1 \
  --api-key $OPENROUTER_API_KEY \
  --api-model google/gemini-3.1-pro-preview
```

Key options:
- `--backend` (`local` | `api`) — Use a local sentence-transformer or an OpenAI-compatible API
- `--model-name` — Embedding model to load (default: `Qwen/Qwen3-Embedding-8B`)
- `--chroma-mode` (`memory` | `persistent` | `http`) — ChromaDB client mode
- `--rp-prompt` / `--hevy-prompt` — Instruction prompts prepended to exercise text

### `port-rp-workout-to-hevy` — Import RP Workouts into Hevy

The core command of the project. Reads every mesocycle from RP's reverse-engineered internal API (no public docs — endpoints were discovered by inspecting the mobile app's network traffic), generates descriptive workout titles via LLM, maps each exercise to its Hevy equivalent using the AI-generated match file, transforms the training history into Hevy workout payloads, and creates (or updates) them via the Hevy API.

```
Usage: port-rp-workout-to-hevy [OPTIONS]

Options:
  --matches PATH              Path to llm-matches.yaml file  [default: data/embeddings/llm-matches.yaml]
  --dry-run                   Show what would be imported without posting
  --start-date [%Y-%m-%d]    Only import days finished on or after this date
  --upsert                    Update existing imported workouts instead of skipping them
  --title-api-base-url TEXT   API base URL for workout title LLM  [required]
  --title-api-key TEXT        API key for workout title LLM  [required]
  --title-api-model TEXT      Model name for workout title LLM  [required]
  --title-concurrency INT     Max concurrent title-generation requests  [default: 10]
  --title-timeout FLOAT       Per-request timeout for title generation (seconds)  [default: 120.0]
  --redis-url TEXT            Redis URL for caching LLM results
```

```bash
# Preview what would be imported
mise //packages/cli:cli port-rp-workout-to-hevy \
  --title-api-base-url https://openrouter.ai/api/v1 \
  --title-api-key $OPENROUTER_API_KEY \
  --title-api-model google/gemini-3-flash-preview \
  --dry-run

# Import everything from January 2026 onwards
mise //packages/cli:cli port-rp-workout-to-hevy \
  --title-api-base-url https://openrouter.ai/api/v1 \
  --title-api-key $OPENROUTER_API_KEY \
  --title-api-model google/gemini-3-flash-preview \
  --start-date 2026-01-01

# With Redis caching for repeated runs
mise //packages/cli:cli port-rp-workout-to-hevy \
  --title-api-base-url https://openrouter.ai/api/v1 \
  --title-api-key $OPENROUTER_API_KEY \
  --title-api-model google/gemini-3-flash-preview \
  --redis-url redis://127.0.0.1:6379 \
  --upsert
```

**How it works:**

1. Loads the AI-generated exercise match file ([`llm-matches.yaml`](../../data/embeddings/llm-matches.yaml)) produced by the embedding pipeline above
2. Fetches all mesocycles from RP's reverse-engineered API (training blocks containing weeks, days, exercises, and sets with weight/reps/RIR)
3. Generates workout titles via LLM — inspects the exercises in each day's first week and produces gym-standard names like "Chest & Triceps", "Pull Day", or "Legs & Glutes". Titles are generated once from the first week and reused across all weeks in the mesocycle. Results are cached in Redis when `--redis-url` is provided
4. Fetches existing Hevy workouts for deduplication (by date and embedded `rp-day-id` tag)
5. Filters days — skips unfinished, skipped, or already-imported days
6. Transforms RP training data into Hevy workout payloads — maps each RP exercise to its Hevy equivalent using the AI match file, converts sets (lb→kg), and clamps duration to 45min–2h
7. Shows a preview table and asks for confirmation
8. Creates or updates workouts via the Hevy API, then prints a summary

**Deduplication:** Each imported workout's description contains an `#import-from-rp` tag and `rp-day-id:<id>` marker. On subsequent runs, days already in Hevy are skipped unless `--upsert` is passed.

**Requirements:** `HEVY_API_KEY`, `RP_BEARER_TOKEN`, and `OPENROUTER_API_KEY` environment variables.

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
  __main__.py        # Click group: rp, hevy, embedding, port
  rp.py              # RP Hypertrophy export commands
  hevy.py            # Hevy export commands
  utils.py           # Shared helpers (token reading, JSON serialization)
  embedding/         # Embedding + similarity search commands
  port/              # RP → Hevy workout importer
    __init__.py      # Re-exports the click command
    models.py        # ExerciseMatch dataclass, constants, YAML loader
    transform.py     # Workout builder, day filtering, duration clamping
    sync.py          # Hevy dedup parsing, summary
    command.py       # Click command + async orchestration
    workout_title_generator.py  # LLM-powered workout title generation
```

## Dependencies

| Package | Purpose |
| --- | --- |
| `click` >=8.1 | CLI framework |
| `pydantic` >=2.12 | Data validation |
| `pydantic-ai` | LLM agent framework (structured output, retries) |
| `api-service` | Async API clients for RP and Hevy (workspace) |
| `embeddings` | Embedding and similarity search library (workspace) |
| `cloudpathlib[s3]` | Cloud storage abstraction (S3, GCS, Azure) |
| `pyyaml` >=6.0 | YAML output for embedding results |
| `ruamel.yaml` | YAML loading for exercise match files |

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
| `RP_BEARER_TOKEN` | *(required)* | RP bearer token (from web app network traffic) |
| `HEVY_API_KEY` | *(required)* | Hevy developer API key |
| `HEVY_API_BASE_URL` | `https://api.hevyapp.com` | Hevy API base URL |
