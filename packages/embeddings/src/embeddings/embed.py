import logging
import os

import torch
import yaml
from sentence_transformers import SentenceTransformer

from embeddings.db import hevy_collection, rp_collection
from embeddings.df import hevy_exercises, rp_exercises

logger = logging.getLogger(__name__)

# 1. Determine the device (use "mps" if available)
device = "mps" if torch.backends.mps.is_available() else "cpu"
logger.info("Using device: %s", device)

# 2. Load the model and move it to the MPS device
logger.info("Loading model paraphrase-mpnet-base-v2")
model = SentenceTransformer(
    "sentence-transformers/paraphrase-mpnet-base-v2", device=device
)

# 3. Encode and store hevy exercises
hevy_docs = hevy_exercises["rich_text_representation"].to_list()
hevy_ids = hevy_exercises["hevy_id"].to_list()
logger.info("Encoding %d hevy exercises", len(hevy_docs))
hevy_embeddings = model.encode(hevy_docs)
logger.debug(
    "Hevy embeddings shape: %s, dtype: %s",
    hevy_embeddings.shape,
    hevy_embeddings.dtype,
)

hevy_collection.add(
    ids=hevy_ids,
    embeddings=hevy_embeddings.tolist(),
    documents=hevy_docs,
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
rp_embeddings = model.encode(rp_docs)
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

final_result = []
for rp_doc, matches, distances in zip(
    rp_docs,
    results["documents"],
    results["distances"],
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

MONOREPO_ROOT = os.environ.get("MONOREPO_ROOT")

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
