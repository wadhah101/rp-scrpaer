import logging
import statistics
from datetime import UTC, datetime
from typing import Any

import chromadb
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_N_RESULTS = 3


def detect_device() -> str:
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    logger.info("Using device: %s", device)
    return device


def load_model(model_name: str, device: str | None = None) -> SentenceTransformer:
    if device is None:
        device = detect_device()
    logger.info("Loading model %s on %s", model_name, device)
    return SentenceTransformer(model_name, device=device)


def encode_and_store(
    model: SentenceTransformer,
    collection: chromadb.Collection,
    docs: list[str],
    ids: list[str],
    prompt: str = "",
    metadatas: list[dict[str, Any]] | None = None,
) -> np.ndarray:
    logger.info("Encoding %d documents", len(docs))
    embeddings = model.encode(docs, prompt=prompt)
    logger.debug("Embeddings shape: %s, dtype: %s", embeddings.shape, embeddings.dtype)

    add_kwargs: dict[str, Any] = {
        "ids": ids,
        "embeddings": embeddings.tolist(),
        "documents": docs,
    }
    if metadatas is not None:
        add_kwargs["metadatas"] = metadatas

    collection.add(**add_kwargs)
    logger.info(
        "Stored %d embeddings, collection count: %d", len(ids), collection.count()
    )
    return embeddings


def query_matches(
    collection: chromadb.Collection,
    query_embeddings: np.ndarray,
    n_results: int = DEFAULT_N_RESULTS,
) -> chromadb.QueryResult:
    logger.info(
        "Querying top-%d matches for %d queries", n_results, len(query_embeddings)
    )
    return collection.query(
        query_embeddings=query_embeddings.tolist(),
        n_results=n_results,
    )


def build_match_results(
    rp_docs: list[str],
    results: chromadb.QueryResult,
) -> list[dict[str, Any]]:
    final = []
    for rp_doc, matches, distances in zip(
        rp_docs,
        results["documents"],
        results["distances"],
        strict=True,
    ):
        final.append(
            {
                "rp_embedding_name": rp_doc,
                "matches": [
                    {"hevy_embedding_name": m, "distance": d}
                    for m, d in zip(matches, distances, strict=True)
                ],
            }
        )
    return final


def compute_metrics(
    *,
    model_name: str,
    rp_prompt: str,
    hevy_prompt: str,
    n_results: int,
    device: str,
    rp_docs: list[str],
    hevy_docs: list[str],
    rp_expected_muscles: list[list[str]],
    results: chromadb.QueryResult,
) -> dict[str, Any]:
    top1_distances: list[float] = []
    confidence_gaps: list[float] = []
    top1_muscle_hits = 0
    topk_muscle_hits = 0

    for expected_muscles, distances, match_metas in zip(
        rp_expected_muscles,
        results["distances"],
        results["metadatas"],
        strict=True,
    ):
        top1_distances.append(distances[0])
        if len(distances) >= 2:
            confidence_gaps.append(distances[1] - distances[0])

        expected = expected_muscles or []
        if match_metas[0].get("primary_muscle_group") in expected:
            top1_muscle_hits += 1
        if any(m.get("primary_muscle_group") in expected for m in match_metas):
            topk_muscle_hits += 1

    n_rp = len(rp_docs)

    return {
        "config": {
            "model": model_name,
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
