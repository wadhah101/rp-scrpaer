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
| **API** (OpenAI-compatible) | Calls a remote embeddings endpoint. Works with Ollama, OpenAI, vLLM, or any OpenAI-compatible server. Supports rate limiting and batching |

Both backends implement the same `Embedder` protocol and are interchangeable. The API backend uses the [OpenAI embeddings API](https://platform.openai.com/docs/api-reference/embeddings), which has become the industry-standard interface for embedding services. This means you can swap providers without changing any code — run `Qwen3-Embedding-8B` locally via Ollama during development, then point at a hosted endpoint in production.

The local backend supports instruction prompts via `--rp-prompt` / `--hevy-prompt` for LLM-based models.

## Current Results

Using `Qwen/Qwen3-Embedding-8B` (fp16) via Ollama, on 315 RP exercises matched against 433 Hevy exercises:

| Metric | Value |
|---|---|
| Muscle group precision@1 | 91.75% |
| Muscle group precision@K | 94.92% |
| Top-1 mean cosine distance | 0.1045 |
| High confidence matches (d < 0.15) | 273 / 315 |
| Ground truth weighted accuracy@1 | 74.74% |
| Ground truth weighted accuracy@K | 88.42% |

See [FUTURE_WORK.md](./FUTURE_WORK.md) for the model evaluation roadmap and pipeline improvements.

## Evaluation

Embedding quality is evaluated at two levels: automated **muscle group precision** (does the top match target the same body part?) and **ground truth accuracy** (does the top match correspond to the correct exercise?). Both run automatically on every embedding pipeline execution.

### Ground truth dataset

A dataset of 100 RP-to-Hevy exercise pairs with human-verified correct matches. Each ground truth file is a YAML document:

```yaml
# ground-truths/bench-press-medium-grip-barbell-chest.yaml
file: bench-press-medium-grip-barbell-chest.yaml
rp_exercise: "bench press medium grip, barbell, chest"
candidates:
  - "bench press - wide grip barbell, chest, shoulders, triceps"
  - "bench press barbell, chest, triceps, shoulders"
  - "bench press - close grip barbell, triceps, chest, shoulders"
best_match: "bench press barbell, chest, triceps, shoulders"
confidence: high
```

Each file records the RP exercise, the top-N Hevy candidates returned by the embedding model, the correct match (or `"none"` if no candidate is valid), and a confidence level (`high`, `medium`, or `low`).

### Generating ground truths with LLM-as-a-judge

The ground truth dataset is generated using Claude as an automated evaluator --- an approach known as [LLM-as-a-judge](https://arxiv.org/abs/2306.05685). The script `claude-as-a-judge.sh` samples exercises from the embedding output, then asks Claude (Sonnet) to pick the best Hevy match for each RP exercise based purely on exercise science knowledge, without seeing distance scores:

```
You are an expert in resistance training and exercise science.
Given an exercise from the RP database, determine which candidate
from the Hevy exercise database is the best match...
```

This is run via GNU `parallel` for throughput (configurable concurrency and sample size). The judge sees only exercise names and candidates --- never the model's distance scores --- so its decisions are independent of the embedding model being evaluated.

### Confidence-weighted metrics

Not all ground truth labels are equally certain. A `"Bench Press (Barbell)"` match is unambiguous; a `"Cable Flye Underhand" → "Low Cable Fly Crossovers"` mapping is debatable. The confidence field captures this:

| Confidence | Weight | Meaning |
|---|---|---|
| `high` | 1.0 | Unambiguous match --- same movement, same equipment |
| `medium` | 0.5 | Reasonable match --- minor variation in name or equipment |
| `low` | 0.0 | Uncertain --- excluded from scoring |

Weighted accuracy avoids penalizing the model for disagreeing with a label that even a human domain expert would find ambiguous.

### Metrics computed

Every pipeline run produces a `metrics.yaml` with:

- **Muscle group precision@1 / @K** --- Does the top (or any top-K) match share the expected primary muscle group? Computed from the muscle group mapping without requiring ground truth labels.
- **Ground truth weighted accuracy@1** --- Among exercises with ground truth labels, what fraction has the correct Hevy exercise as the top-1 match (weighted by confidence)?
- **Ground truth weighted accuracy@K** --- Same, but checking if the correct match appears anywhere in the top-K.
- **Distance statistics** --- Mean, median, stdev, min, max of top-1 cosine distances.
- **Confidence metrics** --- Count of high-confidence (d < 0.15) and low-confidence (d > 0.3) matches, mean confidence gap between top-1 and top-2 distances.
- **Mismatch report** --- Every ground truth exercise where the model's top-1 pick disagrees with the label, with expected vs. actual match and confidence level. This is the primary debugging tool for improving the pipeline.

### Improving accuracy

The evaluation pipeline is designed for iterative improvement:

1. **Run embeddings** with a new model or configuration (`mise //packages/embeddings:embed`)
2. **Check `metrics.yaml`** --- compare muscle group precision and ground truth accuracy against the previous run
3. **Inspect mismatches** --- the mismatch report in `metrics.yaml` shows exactly which exercises regressed and why
4. **Re-generate ground truths** if the candidate set changed (`claude-as-a-judge.sh` re-samples and re-evaluates)

This loop has already driven several improvements: switching from `mxbai-embed-large-v1` (335M params) to `Qwen3-Embedding-8B` (8B params), adding fp16 quantization for faster inference without quality loss, and tuning the muscle group mapping to reduce cross-category false positives.

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

ground-truths/                  # 100 LLM-judged exercise match labels (YAML)
claude-as-a-judge.sh            # Script to generate ground truths using Claude

output/                         # ~314 per-exercise YAML match files (generated)
metrics.yaml                    # Latest evaluation metrics (includes ground truth accuracy)
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
