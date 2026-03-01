# Exercise Matching: RP to Hevy

Semantic exercise matching library that maps exercises from the [RP Hypertrophy](https://rpstrength.com/) app to [Hevy](https://www.hevyapp.com/) using embedding models and vector similarity search.

## Problem

RP and Hevy use different naming conventions for the same exercises:

| RP | Hevy |
|---|---|
| `Bench Press (Medium Grip)` + `exerciseType: "barbell"` | `Bench Press (Barbell)` |
| `Pullup (Underhand Grip)` | `Chin Up` |
| `Machine Flye` | `Butterfly (Pec Deck)` |

Equipment lives in a separate field in RP but is embedded in the exercise title in Hevy. Muscle group taxonomies also differ. Not all RP exercises have a Hevy counterpart.

## Approach

Hybrid strategy: **semantic embeddings + muscle group filtering**.

1. **Load & enrich** --- Build a rich text string per exercise combining name, equipment type, and muscle groups into a single lowercase sentence
2. **Filter by muscle group** --- Join RP exercises with a muscle group mapping (`data/muscle_group_mapping.json`) so candidates are constrained to the same body part
3. **Embed** --- Encode all enriched strings with an embedding model. Supports both local models via `sentence-transformers` and remote OpenAI-compatible APIs
4. **Store & query** --- Index Hevy embeddings in a ChromaDB collection (HNSW, cosine distance). Query with RP embeddings to retrieve the top-N Hevy matches per RP exercise
5. **Evaluate** --- Compute precision@1, precision@K, MRR, and confidence gap metrics
6. **Export** --- Write one YAML file per RP exercise to the output directory

### Embedding backends

| Backend | Description |
|---|---|
| **Local** (`sentence-transformers`) | Loads model on-device (MPS, CUDA, or CPU). Default: `Qwen/Qwen3-Embedding-8B` |
| **API** (OpenAI-compatible) | Calls a remote embeddings endpoint. Supports rate limiting and batching |

Both backends implement the same `Embedder` protocol and are interchangeable. The local backend supports instruction prompts via `--rp-prompt` / `--hevy-prompt` for LLM-based models.

## Current Results

Using `Qwen/Qwen3-Embedding-8B` on 315 RP exercises matched against 433 Hevy exercises:

| Metric | Value |
|---|---|
| Muscle group precision@1 | 91.75% |
| Muscle group precision@K | 94.92% |
| Top-1 mean cosine distance | 0.1035 |
| High confidence matches (d < 0.15) | 277 / 315 |

See [FUTURE_WORK.md](./FUTURE_WORK.md) for the model evaluation roadmap and pipeline improvements.

## Project Structure

```
src/embeddings/
  __init__.py    # Package exports and logging
  schemas.py     # Polars schemas and TypedDicts for RP, Hevy, and muscle group data
  df.py          # Data loading, normalization, joining, and rich text construction
  db.py          # ChromaDB client modes (memory, persistent, HTTP) and collection init
  embed.py       # Embedder protocol, LocalEmbedder, ApiEmbedder, similarity search, metrics

data/
  rp/exercises.json             # 315 RP exercises
  hevy/exercises.json           # 433 Hevy exercises
  muscle_group_mapping.json     # RP muscleGroupId -> Hevy primary_muscle_group

output/                         # ~314 per-exercise YAML match files (generated)
metrics.yaml                    # Latest evaluation metrics
```

## Data Shapes

**RP exercise** (after loading):
```
rp_id | rp_name                      | rp_exerciseType | rp_muscleGroupId
6     | Bench Press (Medium Grip)    | barbell         | 1
```

**Hevy exercise** (after loading):
```
hevy_id  | hevy_title            | hevy_primary_muscle_group | hevy_secondary_muscle_groups
79D0BB3A | Bench Press (Barbell) | chest                     | [triceps, shoulders]
```

**Rich text representation** (fed to the model):
```
RP:   "bench press medium grip, barbell, chest"
Hevy: "bench press barbell, chest, triceps, shoulders"
```

## Setup

Requires Python 3.12+. Install with [uv](https://docs.astral.sh/uv/):

```bash
# macOS / Apple Silicon (MPS acceleration) and CPU
uv sync --extra cpu

# CUDA 13.0
uv sync --extra cu130

# Remote API backend (adds openai dependency)
uv sync --extra api
```

## Usage

The embeddings package is used through the CLI package's `embedding` command group:

```bash
# Embed exercises into persistent ChromaDB
mise //packages/cli:cli embedding embd \
  --backend local --model-name Qwen/Qwen3-Embedding-8B \
  --chroma-mode persistent --chroma-path ./chroma_data

# Run similarity search on already-embedded exercises
mise //packages/cli:cli embedding run-rp-similarity-search \
  --chroma-mode persistent --chroma-path ./chroma_data \
  --metrics-output metrics.yaml --exercise-output-dir output/
```

Or run the standalone entrypoint:

```bash
mise //packages/embeddings:embed
```

### Output format

Each RP exercise produces a separate YAML file:

```yaml
# output/ab-wheel-bodyweight-only-abdominals.yaml
rp_embedding_name: ab wheel, bodyweight-only, abdominals
matches:
  - hevy_embedding_name: ab wheel, abdominals
    distance: 0.1214
  - hevy_embedding_name: torso rotation, abdominals
    distance: 0.2834
  - hevy_embedding_name: reverse crunch, abdominals
    distance: 0.2859
```

Lower distance = better match (cosine distance, 0.0 = identical).

## Dependencies

| Library | Role |
|---|---|
| `sentence-transformers` | Embedding models (local backend) |
| `chromadb` | Vector store with HNSW index (memory, persistent, or HTTP mode) |
| `polars` | DataFrame loading, joins, and transformations |
| `torch` | Tensor backend (MPS / CPU / CUDA) |
| `pydantic` | Data validation schemas |
| `openai` | Remote API backend (optional, via `api` extra) |

## Hardware

Automatically uses Apple Silicon GPU (MPS) when available, falls back to CPU. The dataset is small (~750 exercises total), so a full run completes in under a minute on most machines. Larger models (8B) require 16+ GB memory.
