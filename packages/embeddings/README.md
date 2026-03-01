# Exercise Matching: RP to Hevy

Semantic exercise matching system that maps exercises from the [RP Hypertrophy](https://rpstrength.com/) app to [Hevy](https://www.hevyapp.com/) using sentence-transformer embeddings and vector similarity search.

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
3. **Embed** --- Encode all enriched strings with `paraphrase-mpnet-base-v2` (768-dim, trained on paraphrase detection)
4. **Store & query** --- Index Hevy embeddings in an in-memory ChromaDB collection (HNSW, cosine distance). Query with RP embeddings to retrieve the top 3 Hevy matches per RP exercise
5. **Export** --- Write results to `final_result.yaml`

## Project Structure

```
src/embeddings/
  __init__.py    # Logging configuration
  schemas.py     # Polars schemas and TypedDicts for RP, Hevy, and muscle group data
  df.py          # Data loading, normalization, joining, and rich text construction
  db.py          # ChromaDB client and collection initialization
  embed.py       # Model loading, encoding, similarity search, YAML export

data/
  rp/exercises.json             # ~2000 RP exercises
  hevy/exercises.json           # ~2100 Hevy exercises
  muscle_group_mapping.json     # RP muscleGroupId -> Hevy primary_muscle_group
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
RP:   "bench press (medium grip), barbell, chest"
Hevy: "bench press (barbell), chest, triceps, shoulders"
```

## Setup

Requires Python 3.12+. Install with [uv](https://docs.astral.sh/uv/):

```bash
# macOS / Apple Silicon (MPS acceleration)
uv sync

# CPU-only
uv sync --extra cpu

# CUDA 13.0
uv sync --extra cu130
```

## Usage

```bash
uv run python -m embeddings.embed
```

Output is written to `final_result.yaml`. Each entry looks like:

```yaml
- rp_exercise: "bench press (medium grip), barbell, chest"
  hevy_matches:
    - name: "bench press (barbell), chest, triceps, shoulders"
      distance: 0.0832
    - name: "bench press (dumbbell), chest, triceps, shoulders"
      distance: 0.1145
    - name: "close grip bench press (barbell), chest, triceps, shoulders"
      distance: 0.1290
```

Lower distance = better match (cosine distance, 0.0 = identical).

## Dependencies

| Library | Role |
|---|---|
| `sentence-transformers` | Embedding model (`paraphrase-mpnet-base-v2`) |
| `chromadb` | In-memory vector store with HNSW index |
| `polars` | DataFrame loading, joins, and transformations |
| `torch` | Tensor backend (MPS / CPU / CUDA) |
| `pydantic` | Data validation |

## Hardware

Automatically uses Apple Silicon GPU (MPS) when available, falls back to CPU. The dataset is small (~4k exercises total), so a full run completes in under a minute on most machines.
