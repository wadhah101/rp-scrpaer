# rp-to-hevy

> Extract workout data from [RP Hypertrophy](https://rpstrength.com/) and [Hevy](https://www.hevyapp.com/), match exercises across platforms using semantic embeddings, and convert training history to portable formats.

## The Problem

1. **RP has no public API** — the SDK is reverse-engineered from mobile app traffic.
2. **Hevy's OpenAPI spec is broken** — riddled with violations that block any code generator without [patching](scripts/hevy-extract/README.md) first.
3. **Exercises don't match across platforms** — "Barbell Bench Press" vs "Bench Press (Barbell)" can't be resolved with string matching; [semantic embeddings](packages/embeddings/README.md) solve this.

## Architecture

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

## Packages

| Package | Description |
| ------- | ----------- |
| [`api-service`](packages/api-service/README.md) | Auto-generated async Python SDKs for the RP and Hevy APIs |
| [`cli`](packages/cli/README.md) | Click CLI — exports workouts, runs embedding & similarity search |
| [`embeddings`](packages/embeddings/README.md) | Semantic exercise matching via LLM embeddings + ChromaDB |
| [`pipeline`](packages/pipeline/README.md) | Kestra orchestration — scheduled extraction, S3 triggers, alerts |
| [`hevy-extract`](scripts/hevy-extract/README.md) | Bun/TS tool that fetches & patches the Hevy OpenAPI spec |

## Quick Start

The only prerequisite is [mise](https://mise.jdx.dev/) — it installs all other tools (Python, uv, linters, hk) and is the single source of truth for tool versions across local dev, Docker, and CI.

```bash
curl https://mise.run | sh            # install mise
git clone <repo-url> && cd rp-to-strong
mise install                          # provision all tools
mise prepare                          # uv sync --all-packages
mise lint                             # hk check -a
mise //...:test                       # test every package
```

See [.github/README.md](.github/README.md) for CI/CD pipeline details — remote Docker builds over Tailscale, TruffleHog secret scanning, image tagging, and generated code drift detection.

## References

- [uv Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) — multi-package Python monorepo management
- [mise Monorepo Tasks](https://mise.jdx.dev/tasks/monorepo.html) — task routing with `//path:task` syntax
- [hk Configuration](https://hk.jdx.dev/configuration.html) — Pkl-based git hook configuration
