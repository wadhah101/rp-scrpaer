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

## Model Upgrades: LLM-Based Embedding Models

The default model is now `Qwen/Qwen3-Embedding-8B` (8B params, 4096-dim). This replaced `mixedbread-ai/mxbai-embed-large-v1` (335M params, 1024-dim) which itself replaced the original `paraphrase-mpnet-base-v2`. An OpenAI-compatible API backend is also available via `--backend api`. The remaining frontier is evaluating smaller LLM-based models to find the best quality/cost tradeoff.

### Why LLM-based models

Traditional encoder models (BERT-scale, ~100M--500M params) learn general sentence similarity but have no world knowledge. They treat "RDL" and "Romanian Deadlift" as unrelated tokens unless they happened to co-occur in training data. LLM-based embedders are built on top of pre-trained language models that already understand fitness vocabulary, abbreviations, and equipment relationships. Key advantages:

- **World knowledge** --- They know that "Pullup Underhand Grip" is a "Chin Up", that "Machine Flye" is a "Butterfly (Pec Deck)", and that "RDL" means "Romanian Deadlift". This knowledge is baked into the model weights, not learned from our small dataset.
- **Instruction prompts** --- LLM-based models accept task-specific instructions like `"Given an exercise from the RP app, retrieve the matching Hevy exercise even if it uses alternative names."` This steers the embedding space toward our exact use case without fine-tuning.
- **Higher MTEB scores** --- The best LLM-based models score 70--75 on MTEB English vs. 64--65 for BERT-scale models. On short-text semantic similarity (our task), the gap is even wider.
- **Practical for our dataset** --- We have ~750 exercises. Even an 8B model encodes everything in under a minute on a modern GPU. The extra compute cost is negligible.

### Candidate models by tier

#### Small (0.6B--1.5B params, 1--7 GB)

Best starting point. These run comfortably on CPU or a single consumer GPU and already outperform all BERT-scale models.

| Model | Params | Dim | Size | Notes |
|---|---|---|---|---|
| `Qwen/Qwen3-Embedding-0.6B` | 0.6B | 1024 (MRL 32--1024) | ~1.2 GB | Apache 2.0, 32K context, 100+ languages, instruction-aware |
| `Alibaba-NLP/gte-Qwen2-1.5B-instruct` | 1.5B | 1536 | ~7.1 GB | Strong MTEB for its size, instruction-aware, Apache 2.0 |
| `dunzhang/stella_en_1.5B_v5` | 1.5B | 256--8192 (MRL) | ~6.2 GB | Matryoshka with 8 dimension choices, MIT license |

#### Medium (4B params, ~8 GB)

Sweet spot between quality and resource usage.

| Model | Params | Dim | Size | Notes |
|---|---|---|---|---|
| `Qwen/Qwen3-Embedding-4B` | 4B | 2560 (MRL) | ~8.1 GB | Apache 2.0, instruction-aware, 32K context |

#### Large (7B--8B params, 14--30 GB)

Quality ceiling. Requires a GPU with 16+ GB VRAM (or quantization).

| Model | Params | Dim | Size | Notes |
|---|---|---|---|---|
| `Qwen/Qwen3-Embedding-8B` | 8B | 4096 (MRL 32--4096) | ~15.2 GB | MTEB #1 multilingual (70.58), English 75.22, Apache 2.0 |
| `nvidia/NV-Embed-v2` | 7.85B | 4096 | ~15.7 GB | MTEB English 72.31, novel latent-attention pooling, 32K context. CC-BY-NC-4.0 (non-commercial) |
| `intfloat/e5-mistral-7b-instruct` | 7.1B | 4096 | ~14.2 GB | First major LLM embedder, instruction-aware, MIT license |
| `Salesforce/SFR-Embedding-2_R` | 7.1B | 4096 | ~14.2 GB | Built on e5-mistral, asymmetric retrieval. CC-BY-NC-4.0 |
| `Alibaba-NLP/gte-Qwen2-7B-instruct` | 7B | 3584 | ~30.5 GB | Instruction-tunable, Apache 2.0, needs 16--32 GB VRAM |

### Recommended evaluation order

1. `Qwen3-Embedding-0.6B` --- smallest LLM embedder, fast iteration, likely already better than mxbai
2. `stella_en_1.5B_v5` or `gte-Qwen2-1.5B-instruct` --- 1.5B sweet spot
3. `Qwen3-Embedding-8B` --- quality ceiling, Apache 2.0, best current MTEB scores

Run each against the ground truth (see Evaluation section above). Compare Precision@1, MRR, and inspect failure cases qualitatively. The 0.6B model is the pragmatic first pick; only move to 8B if the 0.6B leaves a meaningful accuracy gap on hard pairs.

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

### ~~Persistent vector store~~ (Done)

~~ChromaDB currently runs in-memory and is rebuilt on every run. Switch to persistent storage (`chromadb.PersistentClient(path="./chroma_db")`) so embeddings only need to be recomputed when the exercise data changes.~~ --- Done: `db.py` supports `memory`, `persistent`, and `http` modes via the `ClientMode` enum. The CLI defaults to `persistent`.

### Many-to-one handling

Multiple RP exercises (grip/angle variants) often map to the same Hevy exercise. The pipeline should detect and flag these explicitly so downstream consumers know which RP exercises share a Hevy match.

### Cross-encoder reranking

After retrieving top-N candidates with the bi-encoder, pass each (RP, Hevy) pair through a cross-encoder (`cross-encoder/stsb-roberta-base` or similar) for a more accurate pairwise similarity score. This is the standard retrieve-then-rerank pattern and typically improves precision by 5-15% on hard pairs.

---

## Synthetic Data and Fine-Tuning

If zero-shot models still fail on edge cases (custom exercises, gym slang, uncommon equipment), fine-tune a small model on synthetic pairs:

1. Use a local LLM (e.g., Llama 3 70B) to generate 3-5k synthetic (RP name, Hevy name) pairs including synonyms, acronyms, and paraphrases
2. Fine-tune `Qwen3-Embedding-0.6B` or `stella_en_1.5B_v5` using contrastive loss
3. Evaluate against the ground truth

This is the "nuclear option" --- only worth pursuing after confirming that zero-shot models leave a meaningful accuracy gap.

---

## Code Quality

- Move YAML export out of `embed.py` into a dedicated output module
- ~~Add a CLI entrypoint (e.g., with `argparse` or `click`) to configure model name, threshold, n_results, and output format~~ --- Done: `packages/cli` has full `embedding embd` and `embedding run-rp-similarity-search` commands
- Add type annotations to DataFrame pipeline return values
- Write integration tests that run on a small fixture dataset
