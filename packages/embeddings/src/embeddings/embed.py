import logging
import os
import statistics
import sys
from datetime import UTC, datetime

import torch
import yaml
from sentence_transformers import SentenceTransformer

from embeddings.db import hevy_collection, rp_collection
from embeddings.df import hevy_exercises, rp_exercises

logger = logging.getLogger(__name__)

# 1. Determine the device (use "mps" if available)
device = "mps" if torch.backends.mps.is_available() else "cpu"
logger.info("Using device: %s", device)

MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"

# 2. Load the model and move it to the MPS device
logger.info("Loading model %s", MODEL_NAME)
model = SentenceTransformer(MODEL_NAME, device=device)

rp_prompt = "You are translating exercise descriptions from english to common exercise names that would make sense across different fitness apps in english"

hevy_prompt = rp_prompt

# 3. Encode and store hevy exercises
hevy_docs = hevy_exercises["rich_text_representation"].to_list()
hevy_ids = hevy_exercises["hevy_id"].to_list()
logger.info("Encoding %d hevy exercises", len(hevy_docs))
hevy_embeddings = model.encode(hevy_docs, prompt=hevy_prompt)
logger.debug(
    "Hevy embeddings shape: %s, dtype: %s",
    hevy_embeddings.shape,
    hevy_embeddings.dtype,
)

hevy_metadatas = [
    {"primary_muscle_group": mg}
    for mg in hevy_exercises["hevy_primary_muscle_group"].to_list()
]
hevy_collection.add(
    ids=hevy_ids,
    embeddings=hevy_embeddings.tolist(),
    documents=hevy_docs,
    metadatas=hevy_metadatas,
)
logger.info(
    "Stored %d hevy embeddings, collection count: %d",
    len(hevy_ids),
    hevy_collection.count(),
)

# 4. Encode and store rp exercises
rp_docs = rp_exercises["rich_text_representation"].to_list()
rp_ids = rp_exercises["rp_id"].cast(str).to_list()
logger.info("Encoding %d rp exercises", len(rp_docs))
rp_embeddings = model.encode(rp_docs, prompt=rp_prompt)
logger.debug(
    "RP embeddings shape: %s, dtype: %s",
    rp_embeddings.shape,
    rp_embeddings.dtype,
)

rp_collection.add(
    ids=rp_ids,
    embeddings=rp_embeddings.tolist(),
    documents=rp_docs,
)
logger.info(
    "Stored %d rp embeddings, collection count: %d",
    len(rp_ids),
    rp_collection.count(),
)

# 5. For each rp exercise, find the most similar hevy exercise
n_results = 3
# TODO: add more logic to queryingm if high confidence 3 is enough, if low confidence, use 10
logger.info(
    "Querying top-%d hevy matches for %d rp exercises",
    n_results,
    len(rp_docs),
)
results = hevy_collection.query(
    query_embeddings=rp_embeddings.tolist(),
    n_results=n_results,
)

# 6. Build results and collect metrics
rp_expected_muscles = rp_exercises["hevy_primary"].to_list()

final_result = []
top1_distances = []
confidence_gaps = []
top1_muscle_hits = 0
topk_muscle_hits = 0

for rp_doc, expected_muscles, matches, distances, match_metas in zip(
    rp_docs,
    rp_expected_muscles,
    results["documents"],
    results["distances"],
    results["metadatas"],
    strict=True,
):
    final_result.append(
        {
            "rp_embedding_name": rp_doc,
            "matches": [
                {"hevy_embedding_name": m, "distance": d}
                for m, d in zip(matches, distances, strict=True)
            ],
        }
    )

    top1_distances.append(distances[0])
    if len(distances) >= 2:
        confidence_gaps.append(distances[1] - distances[0])

    expected = expected_muscles or []
    if match_metas[0].get("primary_muscle_group") in expected:
        top1_muscle_hits += 1
    if any(m.get("primary_muscle_group") in expected for m in match_metas):
        topk_muscle_hits += 1

# 7. Compute and report metrics
n_rp = len(rp_docs)

metrics = {
    "config": {
        "model": MODEL_NAME,
        "rp_prompt": rp_prompt,
        "hevy_prompt": hevy_prompt,
        "n_results": n_results,
        "device": device,
        "n_rp_exercises": n_rp,
        "n_hevy_exercises": len(hevy_docs),
        "timestamp": datetime.now(UTC).isoformat(),
    },
    "distance": {
        "top1_mean": round(statistics.mean(top1_distances), 4),
        "top1_median": round(statistics.median(top1_distances), 4),
        "top1_stdev": round(statistics.stdev(top1_distances), 4),
        "top1_min": round(min(top1_distances), 4),
        "top1_max": round(max(top1_distances), 4),
    },
    "muscle_group_precision": {
        "precision_at_1": round(top1_muscle_hits / n_rp, 4),
        "precision_at_k": round(topk_muscle_hits / n_rp, 4),
        "top1_correct": top1_muscle_hits,
        "topk_correct": topk_muscle_hits,
        "total": n_rp,
    },
    "confidence": {
        "mean_gap": round(statistics.mean(confidence_gaps), 4)
        if confidence_gaps
        else 0,
        "median_gap": round(statistics.median(confidence_gaps), 4)
        if confidence_gaps
        else 0,
        "high_confidence_count": sum(1 for d in top1_distances if d < 0.15),
        "low_confidence_count": sum(1 for d in top1_distances if d > 0.3),
    },
}

os.makedirs("output", exist_ok=True)
with open("metrics.yaml", "w") as f:
    yaml.dump(metrics, f, sort_keys=False, default_flow_style=False)


MONOREPO_ROOT = os.environ.get("MONOREPO_ROOT")
UPDATE_OUTPUT = os.environ.get("UPDATE_OUTPUT", "false").lower() == "true"

if not UPDATE_OUTPUT:
    logger.info("Skipping output update")
    sys.exit(0)

for item in final_result:
    normalized_exercise = (
        (item["rp_embedding_name"].replace(" ", "-").replace(",", "").replace("/", ""))
        .replace(")", "")
        .replace("(", "")
    )
    with open(
        f"{MONOREPO_ROOT}/packages/embeddings/output/{normalized_exercise}.yaml", "w"
    ) as f:
        yaml.dump(item, f, sort_keys=False)
