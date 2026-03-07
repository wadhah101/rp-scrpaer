# rp-to-hevy-cli

Command-line tool for porting workout history from [RP Hypertrophy](https://rpstrength.com/) to [Hevy](https://www.hevyapp.com/). Exports data from both platforms, matches exercises via semantic embeddings, and imports complete training blocks into Hevy. Built with [Click](https://click.palletsprojects.com/) and powered by the workspace packages `api-service` and `embeddings`.

## Why This Exists

RP Hypertrophy has no export feature and no public API. If you want to move your training history to another app, you're stuck. This tool reverse-engineers RP's internal API (discovered by inspecting the mobile app's network traffic), exports everything, and imports it into Hevy with full exercise mapping.

## Hosting and Deployment

A core constraint of this project: I don't want to build an API, handle auth, or expose a public service. I also don't want a scheduled cron job -- if RP detects automated scraping and bans my account, I lose my training data. The import needs to be triggered manually, on my terms.

The solution is a Docker container deployed to **GCP Cloud Run Jobs**. Cloud Run Jobs can be triggered manually from the GCP Console or mobile app, run to completion, and shut down. No always-on infrastructure, no cron, no API surface. I trigger an import when I want one and pay only for the seconds it runs.

The CLI is packaged as a single Docker image (`debian:trixie-slim` runtime, ~830MB) that reads all configuration from environment variables. Cloud Run injects secrets via Secret Manager, and the job runs `port-rp-workout-to-hevy` with the same flags I'd use locally.

## Quick Start

```bash
# Run any command
mise //packages/cli:cli rp export
mise //packages/cli:cli hevy export
mise //packages/cli:cli embedding embd
```

## Command Groups

The CLI has three top-level groups plus a standalone command:

### `rp` -- RP Hypertrophy Export

Export personal workout data from RP Hypertrophy's reverse-engineered internal API to JSON. The API has no public documentation -- endpoints were discovered by inspecting the mobile app's network traffic.

```text
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

### `hevy` -- Hevy Export

Export exercise data from the Hevy app. Requires the `HEVY_API_KEY` environment variable (get it at <https://hevy.com/settings?developer>).

```text
Usage: hevy export [OPTIONS]

Options:
  --type TEXT         Data type to export  [default: all]
  -o, --output PATH   Output file or directory
```

| `--type` | Description |
| --- | --- |
| `all` *(default)* | All data types to a directory |
| `exercise-templates` | Hevy exercise template catalog (~433 exercises) |

### `embedding` -- AI-Powered Exercise Matching

RP and Hevy have completely different exercise catalogs (~315 vs ~433 exercises) with different naming conventions, so we use a multi-stage AI pipeline to match them:

1. **Embed** -- Each exercise is turned into a rich text representation (name + equipment + muscle groups) and encoded into a vector using an OpenAI-compatible embedding API. Vectors are stored in ChromaDB for fast retrieval.
2. **Search** -- For every RP exercise, we query the Hevy collection by cosine similarity and retrieve the top-K nearest candidates.
3. **Judge** -- An LLM (`gemini-3.1-pro-preview` via OpenRouter) reviews each RP exercise and its top-K candidates, then picks the single best match. Results are written to [`data/embeddings/llm-matches.yaml`](../../data/embeddings/llm-matches.yaml) -- a flat list mapping every RP exercise ID/name to a Hevy exercise ID/name with a confidence rating (`high`, `medium`, or `low`).

**`embedding embd`** -- Encode exercises and store in ChromaDB:

```bash
mise //packages/cli:embd
```

**`embedding run-rp-similarity-search`** -- Query already-embedded exercises:

```bash
mise //packages/cli:run-rp-similarity-search
```

**`embedding llm-judge`** -- LLM picks the best match from candidates:

```bash
mise //packages/cli:llm-judge
```

All embedding and LLM API configuration is read from environment variables (`EMBEDDING_API_*`, `JUDGE_API_*`). See the Environment Variables section below.

### ChromaDB

The embeddings package uses [chromadb-client](https://pypi.org/project/chromadb-client/), the HTTP-only thin client for ChromaDB. This avoids pulling in `onnxruntime` and other heavy dependencies that the full `chromadb` package requires for its default embedding function (which we don't use -- we bring our own embedder).

For **local development**, run ChromaDB via Docker Compose:

```bash
docker compose up -d   # starts ChromaDB on localhost:8000
```

In **production**, we use [Chroma Cloud](https://www.trychroma.com/). When `CHROMA_API_KEY` is set, the client automatically switches from `HttpClient` to `CloudClient`.

Configuration is via environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `CHROMA_HOST` | `localhost` | ChromaDB server host (or Chroma Cloud host) |
| `CHROMA_PORT` | `8000` | ChromaDB server port |
| `CHROMA_API_KEY` | *(unset)* | Set to use Chroma Cloud instead of a local server |

### `port-rp-workout-to-hevy` -- Import RP Workouts into Hevy

The core command of the project. Reads every mesocycle from RP's reverse-engineered internal API, generates descriptive workout titles via LLM, maps each exercise to its Hevy equivalent using the AI-generated match file, transforms the training history into Hevy workout payloads, and creates (or updates) them via the Hevy API.

```text
Usage: port-rp-workout-to-hevy [OPTIONS]

Options:
  --matches PATH              Path to llm-matches.yaml file  [default: data/embeddings/llm-matches.yaml]
  --dry-run                   Show what would be imported without posting
  --start-date [%Y-%m-%d]    Only import days finished on or after this date
  --upsert                    Update existing imported workouts instead of skipping them
  --title-concurrency INT     Max concurrent title-generation requests  [default: 10]
  --title-timeout FLOAT       Per-request timeout for title generation (seconds)  [default: 120.0]
  --cache-url TEXT            Cache database URL  [default: sqlite+libsql:///data/cache.db]
  --yes, -y                   Skip confirmation prompt
```

```bash
# Preview what would be imported
mise //packages/cli:cli port-rp-workout-to-hevy --dry-run

# Import everything from January 2026 onwards
mise //packages/cli:cli port-rp-workout-to-hevy --start-date 2026-01-01
```

**How it works:**

1. Loads the AI-generated exercise match file ([`llm-matches.yaml`](../../data/embeddings/llm-matches.yaml)) produced by the embedding pipeline above
2. Fetches all mesocycles from RP's reverse-engineered API (training blocks containing weeks, days, exercises, and sets with weight/reps/RIR)
3. Generates workout titles via LLM -- inspects the exercises in each day's first week and produces gym-standard names like "Chest & Triceps", "Pull Day", or "Legs & Glutes". Titles are generated once from the first week and reused across all weeks in the mesocycle. Results are cached in the LLM response cache (see below)
4. Fetches existing Hevy workouts for deduplication (by date and embedded `rp-day-id` tag)
5. Filters days -- skips unfinished, skipped, or already-imported days
6. Transforms RP training data into Hevy workout payloads -- maps each RP exercise to its Hevy equivalent using the AI match file, converts sets (lb to kg), and clamps duration to 45min-2h
7. Shows a preview table and asks for confirmation
8. Creates or updates workouts via the Hevy API, then prints a summary

**Deduplication:** Each imported workout's description contains an `#import-from-rp` tag and `rp-day-id:<id>` marker. On subsequent runs, days already in Hevy are skipped unless `--upsert` is passed.

## LLM Response Cache

LLM calls (workout title generation, exercise judging) are cached in a SQLite database via SQLAlchemy. This avoids re-calling the LLM for the same prompt across runs, which matters when iterating on import logic or re-running after a partial failure.

Locally, the cache defaults to a SQLite file (`data/cache.db`). In production, we use [Turso](https://turso.tech/) -- a hosted libSQL service that gives us a persistent, globally-replicated cache database without managing infrastructure. The `sqlalchemy-libsql` dialect connects to Turso via its HTTP API, authenticated by `TURSO_AUTH_TOKEN`.

The cache is keyed by `(namespace, sha256(prompt))`, where namespace includes the model name to avoid collisions when switching models.

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
| `embd` | Embed exercises into ChromaDB |
| `run-rp-similarity-search` | Run similarity search on embedded exercises |
| `llm-judge` | Use LLM to pick the best match per exercise |
| `export-rp-local` | Export all RP data to `exports/rp/` |
| `export-rp-s3` | Export all RP data to S3 (requires `BUCKET_NAME`) |
| `export-hevy-local` | Export Hevy exercises to `exports/hevy/` |
| `export-hevy-s3` | Export Hevy exercises to S3 (requires `BUCKET_NAME`) |
| `port-rp-workout-to-hevy` | Port RP workouts to Hevy |
| `build` | Build the Docker image |

## Package Structure

```text
src/rp_to_hevy_cli/
  __main__.py        # Click group: rp, hevy, embedding, port
  rp.py              # RP Hypertrophy export commands
  hevy.py            # Hevy export commands
  settings.py        # Environment variable configuration
  utils.py           # YAML and JSON serialization helpers
  cache.py           # LLM response cache (SQLAlchemy + libSQL)
  agent.py           # LLM agent runner with retries and caching
  embedding/         # Embedding + similarity search commands
  port/              # RP -> Hevy workout importer
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
| `pydantic-ai-slim[openai]` | LLM agent framework (structured output, retries) |
| `api-service` | Async API clients for RP and Hevy (workspace) |
| `embeddings[api]` | Embedding and similarity search library (workspace) |
| `cloudpathlib[s3,gs]` | Cloud storage abstraction (S3, GCS, Azure) |
| `pyyaml` >=6.0 | YAML output for embedding results |
| `ruamel-yaml` | YAML loading for exercise match files |
| `sqlalchemy` >=2.0 | Database ORM for LLM response caching |
| `sqlalchemy-libsql` | SQLAlchemy dialect for libSQL/Turso |

The `embeddings` package uses `chromadb-client` (HTTP-only, no `onnxruntime`) instead of the full `chromadb` package.

Requires **Python >= 3.12**.

## Docker

```bash
# Build only
mise //packages/cli:build

# Build + TruffleHog scan + push to registry
mise //packages/cli:build-push
```

3-stage build (mise -> builder -> `debian:trixie-slim` runtime):

- **`uv sync --frozen --compile-bytecode`** -- reproducible installs with pre-compiled `.pyc` for fast startup
- **Test and metadata stripping** -- test suites and unused Python stdlib modules (`idlelib`, `lib2to3`, `ensurepip`) are removed from the final image
- **TruffleHog secret scan** gates every push -- images are built locally (`--load`), scanned, then pushed only if clean
- **Non-root runtime** -- runs as `app` user
- **Flat `/app/packages/` source copy** -- all workspace `src/` dirs copied to a single directory with `PYTHONPATH` resolution

## Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `RP_APP_BASE_URL` | `https://training.rpstrength.com/api` | RP API base URL |
| `RP_APP_VERSION` | `1.1.13` | `accept-version` header value |
| `RP_BEARER_TOKEN` | *(required)* | RP bearer token (from web app network traffic) |
| `HEVY_API_KEY` | *(required)* | Hevy developer API key |
| `HEVY_API_BASE_URL` | `https://api.hevyapp.com` | Hevy API base URL |
| `EMBEDDING_API_BASE_URL` | *(required for embd)* | Embedding API base URL |
| `EMBEDDING_API_KEY` | *(required for embd)* | Embedding API key |
| `EMBEDDING_API_MODEL` | *(required for embd)* | Embedding model name |
| `EMBEDDING_API_DIMENSIONS` | *(unset)* | Embedding dimensions (optional) |
| `EMBEDDING_API_BATCH_SIZE` | `100` | Embedding API batch size |
| `JUDGE_API_BASE_URL` | *(required for llm-judge)* | Judge LLM API base URL |
| `JUDGE_API_KEY` | *(required for llm-judge)* | Judge LLM API key |
| `JUDGE_API_MODEL` | *(required for llm-judge)* | Judge LLM model name |
| `TITLE_API_BASE_URL` | *(required for port)* | Title generation LLM API base URL |
| `TITLE_API_KEY` | *(required for port)* | Title generation LLM API key |
| `TITLE_API_MODEL` | *(required for port)* | Title generation LLM model name |
| `CHROMA_HOST` | `localhost` | ChromaDB server host |
| `CHROMA_PORT` | `8000` | ChromaDB server port |
| `CHROMA_API_KEY` | *(unset)* | Chroma Cloud API key (enables CloudClient) |
| `TURSO_AUTH_TOKEN` | *(optional)* | Auth token for remote Turso cache database |
