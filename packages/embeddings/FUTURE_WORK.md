# Future Work

Improvements and evaluation strategies for the exercise matching pipeline.

## Evaluation

There is currently no quantitative evaluation. Before changing models or logic, build a ground truth and measure against it.

### Build a ground truth dataset

Manually label 100-200 RP-to-Hevy pairs as correct/incorrect. Include easy matches ("Barbell Curl" -> "Bicep Curl (Barbell)"), hard synonyms ("Pullup Underhand Grip" -> "Chin Up"), and known non-matches. Store as a simple CSV.

### Metrics

- **Precision@1** --- Is the top match correct?
- **Precision@3** --- Is the correct match in the top 3?
- **Mean Reciprocal Rank (MRR)** --- Where does the correct match rank on average?
- **Unmatched rate** --- How many RP exercises have no valid Hevy match above the confidence threshold?

Run every model/config change against this ground truth to catch regressions.

---

## Model Upgrades

### Paraphrase models (current tier)

The pipeline uses `paraphrase-mpnet-base-v2` (768-dim, ~420 MB). This is strong for synonym detection but there are better options in the same weight class:

| Model | Dim | Size | Advantage |
|---|---|---|---|
| `paraphrase-MiniLM-L6-v2` | 384 | 80 MB | 5x faster, minimal quality loss --- good for rapid iteration |
| `BAAI/bge-small-en-v1.5` | 384 | 130 MB | Top MTEB performer in the small tier. Supports instruction prefixes like `"Represent this exercise for matching:"` which can steer embeddings toward the task |
| `BAAI/bge-base-en-v1.5` | 768 | 440 MB | Same family, stronger. Instruction prefix support |
| `intfloat/e5-small-v2` / `e5-base-v2` | 384/768 | 130/440 MB | Microsoft E5 models, strong on short text. Require `"query: "` / `"passage: "` prefixes |
| `nomic-ai/nomic-embed-text-v1.5` | 768 | 550 MB | Matryoshka embeddings --- can truncate dimensions (768 -> 256 -> 128) without retraining for speed/quality tradeoff |

### LLM-based embedding models

For maximum zero-shot quality, LLM-based embedders understand fitness vocabulary natively (they know "RDL" = "Romanian Deadlift"):

| Model | Params | Why |
|---|---|---|
| `Alibaba-NLP/gte-Qwen2-7B-instruct` | 7B | Top MTEB. Highly instruction-tunable: `"Given an exercise from the RP app, retrieve the matching Hevy exercise even if it uses alternative names."` |
| `Salesforce/SFR-Embedding-Mistral` | 7B | Built on Mistral-7B, designed for asymmetric retrieval (query looks different from document) |
| `mixedbread-ai/mxbai-embed-large-v1` | ~335M | 1024-dim, Matryoshka support. Peak traditional encoder quality without going to 7B parameters |

The dataset is tiny (~4k exercises), so even a 7B model encodes everything in a few minutes on a modern GPU.

### Benchmarking plan

Run all candidate models against the ground truth. Compare Precision@1, MRR, and inspect the failure cases qualitatively. Likely priority order:

1. `paraphrase-mpnet-base-v2` (current baseline)
2. `BAAI/bge-small-en-v1.5` (instruction prefix, lightweight)
3. `paraphrase-MiniLM-L6-v2` (speed baseline)
4. `gte-Qwen2-7B-instruct` (quality ceiling)

---

## Pipeline Improvements

### Confidence threshold and manual review

Currently all top-3 matches are exported without filtering. Add a configurable similarity threshold (e.g., 0.3 cosine distance) and split results into:
- **High confidence** (distance < 0.15): auto-accept
- **Medium confidence** (0.15 - 0.35): flag for review
- **Low confidence** (> 0.35): treat as unmatched

Export the medium-confidence band to a separate file for manual verification.

### Muscle group filtering at query time

The muscle group join happens at the DataFrame level but is not enforced during the ChromaDB query. All Hevy exercises are searched regardless of muscle group. Implementing per-muscle-group collections (or ChromaDB metadata filtering with `where={"primary_muscle_group": ...}`) would reduce false positives --- a "Press" in chest won't match a "Press" in shoulders.

### Persistent vector store

ChromaDB currently runs in-memory and is rebuilt on every run. Switch to persistent storage (`chromadb.PersistentClient(path="./chroma_db")`) so embeddings only need to be recomputed when the exercise data changes.

### Many-to-one handling

Multiple RP exercises (grip/angle variants) often map to the same Hevy exercise. The pipeline should detect and flag these explicitly so downstream consumers know which RP exercises share a Hevy match.

### Cross-encoder reranking

After retrieving top-N candidates with the bi-encoder, pass each (RP, Hevy) pair through a cross-encoder (`cross-encoder/stsb-roberta-base` or similar) for a more accurate pairwise similarity score. This is the standard retrieve-then-rerank pattern and typically improves precision by 5-15% on hard pairs.

---

## Synthetic Data and Fine-Tuning

If zero-shot models still fail on edge cases (custom exercises, gym slang, uncommon equipment), fine-tune a small model on synthetic pairs:

1. Use a local LLM (e.g., Llama 3 70B) to generate 3-5k synthetic (RP name, Hevy name) pairs including synonyms, acronyms, and paraphrases
2. Fine-tune `bge-small-en-v1.5` or `paraphrase-MiniLM-L6-v2` using contrastive loss or SetFit
3. Evaluate against the ground truth

This is the "nuclear option" --- only worth pursuing after confirming that zero-shot models leave a meaningful accuracy gap.

---

## Code Quality

- Move YAML export out of `embed.py` into a dedicated output module
- Add a CLI entrypoint (e.g., with `argparse` or `click`) to configure model name, threshold, n_results, and output format
- Add type annotations to DataFrame pipeline return values
- Write integration tests that run on a small fixture dataset
