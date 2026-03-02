# rp-to-hevy

> **Showcase project** demonstrating the best modern Python tooling: [uv](https://docs.astral.sh/uv/) workspaces, [mise](https://mise.jdx.dev/) monorepo tasks, [hk](https://hk.jdx.dev/) git hooks, multi-stage Docker builds, and GitHub Actions CI — all wired together into a single, reproducible developer experience.

Extract workout data from the [RP Hypertrophy](https://rpstrength.com/) and [Hevy](https://www.hevyapp.com/) apps, match exercises across platforms using semantic embeddings, and convert training history to portable formats. The CLI handles on-demand exports; a [Kestra](https://kestra.io/) pipeline adds scheduled extraction with event-driven orchestration, S3 triggers, failure handling, and user notifications.

## The Problem

[RP Hypertrophy](https://rpstrength.com/) and [Hevy](https://www.hevyapp.com/) are fitness apps for tracking strength-training workouts. RP programs your mesocycles and auto-regulates volume; Hevy is a general-purpose workout logger with social features. Both store your training history, but neither makes it easy to get your data out — and moving between them is even harder.

Three specific problems make this project necessary:

1. **RP has no public API.** There is no documented developer interface. The SDK in [`packages/api-service`](packages/api-service/README.md) is built against a private API that was reverse-engineered from the mobile app's network traffic. Endpoints, auth flows, and payload shapes were discovered by inspecting requests — nothing is guaranteed to be stable, and there are no official docs to fall back on.

2. **Hevy's OpenAPI spec is broken.** Hevy *does* publish API docs at `api.hevyapp.com/docs`, but the spec is embedded inside a Swagger UI init script and riddled with violations: missing `operationId` on every endpoint, parameters without `schema`, `type: "enum"` instead of `type: "string"`, per-property `required: true` booleans instead of a proper `required` array, and `$ref` nodes with illegal sibling properties. The spec cannot be fed to any code generator without significant patching first — which is exactly what [`scripts/hevy-extract/`](scripts/hevy-extract/README.md) does.

3. **Exercises don't match across platforms.** RP calls it "Barbell Bench Press", Hevy calls it "Bench Press (Barbell)". Multiply that across hundreds of exercises and there is no reliable way to map one catalog to the other with string matching alone. The [`embeddings`](packages/embeddings/README.md) package solves this with LLM-based semantic embeddings and vector similarity search.

## The Core Idea: One Source of Truth, Everywhere

The defining principle of this repo is that **`.mise.tools.toml` is the single source of truth** for every tool version — on your laptop, in Docker, and in CI. There is no second place where Python 3.12 or uv 0.10.7 is declared. The root `.miserc.toml` is the entrypoint — it loads three split config files: `.mise.env.toml` (environment, monorepo settings), `.mise.tools.toml` (tool versions), and `.mise.tasks.toml` (tasks). Every environment reads these same files.

Change `python = "3.12"` in `.mise.tools.toml` and **every developer machine, every Docker image, and every CI run** picks it up. Zero drift, zero duplication.

## Monorepo Architecture

This project is a **uv + mise driven Python monorepo** — uv manages Python packages and dependencies, mise orchestrates tasks and tool versions, and hk runs lightning-fast git hooks.

### How the packages fit together

```
  ┌──────────────────────────────────────────────────────────┐
  │                      RP & Hevy APIs                      │
  └──────────────┬──────────────────────────┬────────────────┘
                 │                          │
       ┌─────────▼─────────┐    ┌──────────▼──────────┐
       │   api-service      │    │   api-service        │
       │  (RP SDK)          │    │  (Hevy SDK)          │
       └─────────┬─────────┘    └──────────┬──────────┘
                 │                          │
       ┌─────────▼──────────────────────────▼──────────┐
       │                    cli                         │
       │  rp export · hevy export · embedding commands  │
       └─────────┬──────────────────────────┬──────────┘
                 │                          │
       ┌─────────▼─────────┐    ┌──────────▼──────────┐
       │   embeddings       │    │   pipeline            │
       │  Similarity search │    │  Kestra scheduled    │
       │  ChromaDB + LLM    │    │  extraction + flows  │
       └───────────────────┘    └─────────────────────┘
```

- **[`api-service`](packages/api-service/README.md)** --- Auto-generated async Python SDKs for the RP and Hevy APIs, produced from OpenAPI specs. The foundation that all other packages build on.
- **[`cli`](packages/cli/README.md)** --- Click-based CLI frontend. Exports workout data to JSON (local or cloud storage), runs embedding and similarity search. The primary user-facing interface today.
- **[`embeddings`](packages/embeddings/README.md)** --- Semantic exercise matching library. Encodes RP and Hevy exercises with LLM-based embedding models, stores them in ChromaDB, and finds the best cross-platform matches. Achieves 91.75% muscle group precision@1 with `Qwen/Qwen3-Embedding-8B`.
- **[`pipeline`](packages/pipeline/README.md)** --- [Kestra](https://kestra.io/) orchestration layer. Runs the same data extraction as the CLI but on a schedule with event-driven S3 triggers, automatic retries, failure alerts, and user notifications. Flows are declarative YAML definitions synced to the Kestra server via Docker Compose.

## Quick Start

The only prerequisite is [mise](https://mise.jdx.dev/). Everything else — Python, uv, linters, hk — is installed automatically.

```bash
# Install mise (if you don't have it)
curl https://mise.run | sh

# Clone and setup — mise installs all tools, uv syncs all packages
git clone <repo-url> && cd rp-to-strong
mise install
mise prepare          # runs: uv sync --all-packages

# Verify everything works
mise lint             # runs: hk check -a
mise //...:test       # runs tests in every package
```

## uv Workspace

The root `pyproject.toml` declares a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/) that groups all packages under a **single lockfile** (`uv.lock`):

### How the workspace fits together

| Package                 | Path                    | Description                                     | Workspace dependencies            |
| ----------------------- | ----------------------- | ----------------------------------------------- | --------------------------------- |
| `rp-to-strong`          | *(root)*                | Workspace root                                  | all below                         |
| [`api-service`](packages/api-service/README.md)           | `packages/api-service`  | Auto-generated async API SDKs (RP + Hevy)       | External only                     |
| [`embeddings`](packages/embeddings/README.md)            | `packages/embeddings`   | Semantic exercise matching (ChromaDB + LLM)     | External only                     |
| [`rp-to-strong-cli`](packages/cli/README.md)      | `packages/cli`          | Click CLI frontend                              | `api-service`, `embeddings`       |

Key properties of uv workspaces:

- **Single lockfile** — `uv lock` resolves all members together into one `uv.lock`, guaranteeing consistent dependency versions across the entire monorepo.
- **Editable installs** — workspace member cross-references (e.g. cli depending on api-service and embeddings) are installed as editable packages automatically.
- **Targeted operations** — `uv sync --package rp-to-strong-cli` installs only what one package needs (used in Docker builds).
- **Shared `requires-python`** — all members must agree on `>=3.12`, enforced by uv as the intersection of all member constraints.

Reference: [uv Workspaces documentation](https://docs.astral.sh/uv/concepts/projects/workspaces/)

## mise: Tool Versions and Monorepo Tasks

mise is the **single entry point** for all developer tooling. It replaces pyenv, nvm, Makefiles, and task runners with one config file.

### Tool management

The root `.mise.tools.toml` declares every tool the project needs (loaded via `.miserc.toml` → `env`, `tools`, `tasks` split):

`mise install` provisions **all of these** in one shot — no brew, no pip install, no manual downloads. Every version is pinned explicitly in `.mise.tools.toml` for reproducibility.

### How Python versions flow from mise to containers

This is the key design: **mise is the single source of truth for the Python version**, both locally and in Docker. There is no `.python-version` file, no hardcoded `FROM python:3.12` image tag, no separate version matrix in CI.

```
.mise.tools.toml (root)
  python = "3.12"
       |
       ├──> Local dev
       │    `mise install`
       │
       ├──> Dockerfile
       │    COPY .miserc.toml .mise.env.toml .mise.tools.toml ./
       │    RUN mise install python uv
       │
       └──> CI
            jdx/mise-action reads .miserc.toml → .mise.tools.toml
```

Inside each Dockerfile, the builder stage:

1. Copies the `jdxcode/mise` binary from its official image
2. Copies the **root** `.miserc.toml`, `.mise.env.toml`, and `.mise.tools.toml` into the container
3. Runs `mise install python uv` — which reads the exact same pinned versions
4. Extracts the installed Python to `/opt/python` for the runtime stage

The same flow applies in CI: `jdx/mise-action` reads `.miserc.toml` (which loads `.mise.tools.toml`) and installs identical tool versions. **One file to bump, three environments updated.**

### Monorepo task routing

mise's [experimental monorepo](https://mise.jdx.dev/tasks/monorepo.html) feature automatically discovers `.mise.toml` files in subdirectories and namespaces their tasks by path

This creates a flat, routable task namespace:

```bash
# Run a task in a specific package
mise //packages/pipeline:build
mise //packages/cli:test

# Run a task in ALL packages (the ... wildcard)
mise //...:test          # test everything
mise //...:build         # build everything

# Root-level tasks
mise lint                # hk check -a
mise prepare             # uv sync --all-packages
```

The `//...:` syntax is what CI uses — `mise //...:test` in the test workflow and `mise //...:build` in the build workflow. One command, every package, zero config duplication.

### mise prepare

The `[prepare]` block runs setup tasks that should execute before anything else:

```toml
[prepare.uv]
run = "uv sync --all-packages"
```

`mise prepare` bootstraps the workspace — installs all Python dependencies into the shared `.venv` so every package is ready to use immediately.

## hk: Fast Git Hooks

[hk](https://hk.jdx.dev/) is a git hook manager written in Rust by the same author as mise. It is **fast** — hk runs all linters in parallel by default, only on files that match each linter's glob/type filter, and only on staged files in pre-commit hooks. Where pre-commit (Python) might take 5-10 seconds on a typical run, hk finishes in under a second for incremental changes.

## Docker Builds

Packages with a Dockerfile use 3-stage builds following the same pattern:

```
Stage 1: mise          Grab the mise binary from jdxcode/mise:2026.2.23
Stage 2: builder       Install Python+uv via mise, uv sync, copy source
Stage 3: runtime       Minimal debian:trixie-slim with just Python + .venv
```

The critical detail is in stage 2 — the builder **does not hardcode any tool versions**. It copies the split mise config from the repo root and runs `mise install`, so the container always matches local dev:

```dockerfile
COPY .miserc.toml .mise.env.toml .mise.tools.toml ./
RUN mise install python uv
```

Other techniques used:

- **`syntax=docker/dockerfile:1.13-labs`** — enables `COPY --parents` for preserving directory structure when copying `pyproject.toml` files
- **`uv sync --frozen --package <name> --no-editable --compile-bytecode`** — installs only the target package's dependencies from the locked `uv.lock`, no editable installs (production mode), and pre-compiles `.pyc` files for faster startup
- **`PYTHONDONTWRITEBYTECODE=1`** — since bytecode is already compiled at build time, the runtime container is fully immutable (no `.pyc` written at runtime)
- **Flat `/app/packages/` copy** — all workspace package `src/` directories are copied to a single flat directory, with `PYTHONPATH` set to resolve imports. This avoids copying full package directories with their own `pyproject.toml`, tests, and configs into the runtime image
- **`--mount=type=secret,id=GITHUB_TOKEN`** — BuildKit secret mounts pass GitHub tokens for private dependency resolution without baking them into layers
- **Non-root runtime** — `useradd -r app` + `USER app` for security
- **Pinned base images** — `debian:trixie-slim@sha256:...` with pinned `apt` package versions for reproducible builds

### Building

```bash
# Build all images
mise //...:build

# Build a specific package
mise //packages/cli:build

# Build + TruffleHog scan + push to registry
mise //packages/cli:build-push
```

## [scripts/hevy-extract](scripts/hevy-extract/README.md): OpenAPI Spec Extraction

A standalone Bun/TypeScript tool that fetches the Hevy OpenAPI spec from their Swagger UI docs page, fixes every spec violation, and outputs clean JSON ready for code generation.

The Hevy docs page loads a `swagger-ui-init.js` script with the full OpenAPI spec embedded inline. Rather than parsing the JS as text, the extractor evaluates it in a sandbox with mocked Swagger UI globals. When the script calls `SwaggerUIBundle(opts)`, the mock intercepts and captures `opts.spec`. This is resilient to formatting changes since it relies on runtime behavior, not string patterns.

After extraction, these fixes are applied automatically:

| Fix | What it does |
|-----|--------------|
| `addOperationIds` | Generates `operationId` for every endpoint (`getWorkouts`, `postRoutines`, etc.) |
| `fixMissingParameterSchemas` | Adds `{ type: "string" }` to parameters with no `schema` |
| `fixEnumSchemaTypes` | Replaces non-standard `type: "enum"` with `type: "string"` |
| `fixBooleanRequired` | Converts per-property `required: true` into a proper `required` array on the parent |
| `fixRefSiblings` | Wraps `$ref` nodes that have sibling properties into `allOf` |

The output feeds into the SDK generation pipeline via mise tasks:

```
scripts/hevy-extract/extract.ts    →  openapi.json (patched spec)
    → yq -p json -o yaml           →  packages/api-service/openapi/hevy.openapi.yaml
    → openapi-generator-cli        →  packages/api-service/src/hevy_api_service/ (async Python SDK)
```

```bash
# Run directly
cd scripts/hevy-extract && bun run start

# Or through mise (also triggers the YAML conversion)
mise //scripts/hevy-extract:export
```

## CI/CD

Three GitHub Actions workflows, all driven by mise:

| Workflow  | Runs                           | Command                           |
| --------- | ------------------------------ | --------------------------------- |
| **lint**  | hk check on all files          | `hk check --all`                  |
| **test**  | Tests in every package         | `mise prepare && mise //...:test` |
| **build** | Docker build + scan + push     | `mise run build-push`             |

All workflows use `jdx/mise-action` to install mise from the **same `.miserc.toml` → `.mise.tools.toml`**, which then provisions all other tools. No manual tool installation steps in CI, no version matrices, no cache configuration — the same single source of truth applies here too.

### What makes this pipeline interesting

- **ARM-native builds** — The build workflow runs on Blacksmith 4-vCPU ARM runners (`blacksmith-4vcpu-ubuntu-2404-arm`), producing native ARM Docker images with zero QEMU emulation overhead.

- **Build → Scan → Push gating** — Every image is built locally (`docker buildx build --load`), scanned by [TruffleHog](https://github.com/trufflesecurity/trufflehog) for leaked secrets, and only pushed to the registry if the scan passes. The `--load` + separate push adds ~30-60s vs `buildx --push`, but guarantees no secret ever reaches the registry. This is defined in the `build-push` task template in `.mise.tasks.toml`.

- **Intelligent image tagging** — Tags combine `GIT_SHA_SHORT` (short commit hash) + `GIT_DIFF_HASH` (SHA-1 of `git diff HEAD`). The `master` branch normalizes to `latest`. Non-alphanumeric branch characters become hyphens. This means every build — even with uncommitted local changes — gets a unique, traceable tag. CI additionally passes `$GIT_SHA_SHORT` and `$GIT_BRANCH_NORM` as explicit tags.

- **Generated code drift detection** — The `generate-no-diff` job in the lint workflow re-runs all code generation (`mise "//...:generate-libs*"`), formats the output, then asserts `git status --porcelain` is empty. This catches stale generated code that someone forgot to commit.

- **Minimal CI config** — All 3 workflows delegate to `mise` commands. No tool installation steps, no version matrices, no cache configuration — `jdx/mise-action` reads `.miserc.toml` → `.mise.tools.toml` and handles everything.

- **Local CI simulation** — `mise all-ci` runs the full pipeline locally: generate → format → lint + build + test in parallel. The same commands CI runs, on your machine.

- **Security hardening** — BuildKit secret mounts for tokens (never baked into layers), non-root containers (`USER app`), pinned base image digests with SHA-256, and pinned apt package versions.

## References

- [uv Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) — how uv manages multi-package Python monorepos
- [mise Monorepo Tasks](https://mise.jdx.dev/tasks/monorepo.html) — task routing with `//path:task` syntax
- [hk Configuration](https://hk.jdx.dev/configuration.html) — Pkl-based git hook configuration
