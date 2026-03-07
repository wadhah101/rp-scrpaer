from __future__ import annotations

import logging
import os
import statistics
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import chromadb
import numpy as np

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_N_RESULTS = 3


@runtime_checkable
class Embedder(Protocol):
    def encode(self, texts: list[str], *, prompt: str = "") -> np.ndarray: ...


class LocalEmbedder(Embedder):
    """Wraps ``SentenceTransformer`` to satisfy the :class:`Embedder` protocol."""

    def __init__(self, model: SentenceTransformer) -> None:
        self.model = model

    def encode(self, texts: list[str], *, prompt: str = "") -> np.ndarray:
        return self.model.encode(texts, prompt=prompt)


def create_local_embedder(model_name: str, device: str | None = None) -> LocalEmbedder:
    model = load_model(model_name, device)
    return LocalEmbedder(model)


@dataclass
class RateLimitConfig:
    batch_size: int = 100


class ApiEmbedder(Embedder):
    """Calls an OpenAI-compatible embeddings API."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        dimensions: int | None = None,
        rate_limit: RateLimitConfig | None = None,
    ) -> None:
        from openai import OpenAI

        self._client = OpenAI(base_url=base_url, api_key=api_key)
        self._model = model
        self._dimensions = dimensions
        self._rate_limit = rate_limit or RateLimitConfig()

    def encode(self, texts: list[str], *, prompt: str = "") -> np.ndarray:
        if prompt:
            texts = [prompt + t for t in texts]

        all_embeddings: list[list[float]] = []
        batch_size = self._rate_limit.batch_size

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            kwargs: dict[str, Any] = {"input": batch, "model": self._model}
            if self._dimensions is not None:
                kwargs["dimensions"] = self._dimensions

            response = self._client.embeddings.create(**kwargs)
            all_embeddings.extend([d.embedding for d in response.data])

        return np.array(all_embeddings, dtype=np.float32)


def detect_device() -> str:
    import torch

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    logger.info("Using device: %s", device)
    return device


def load_model(model_name: str, device: str | None = None) -> SentenceTransformer:
    from sentence_transformers import SentenceTransformer as _ST

    if device is None:
        device = detect_device()
    logger.info("Loading model %s on %s", model_name, device)
    return _ST(model_name, device=device)


def encode_and_store(
    embedder: Embedder,
    collection: chromadb.Collection,
    docs: list[str],
    ids: list[str],
    prompt: str = "",
    metadatas: list[dict[str, Any]] | None = None,
) -> np.ndarray:
    logger.info("Encoding %d documents", len(docs))
    embeddings = embedder.encode(docs, prompt=prompt)
    logger.debug("Embeddings shape: %s, dtype: %s", embeddings.shape, embeddings.dtype)

    BATCH_SIZE = 300
    emb_list = embeddings.tolist()
    for i in range(0, len(ids), BATCH_SIZE):
        batch: dict[str, Any] = {
            "ids": ids[i : i + BATCH_SIZE],
            "embeddings": emb_list[i : i + BATCH_SIZE],
            "documents": docs[i : i + BATCH_SIZE],
        }
        if metadatas is not None:
            batch["metadatas"] = metadatas[i : i + BATCH_SIZE]
        collection.upsert(**batch)

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
    rp_docs: list[dict[str, str]],
    results: chromadb.QueryResult,
) -> list[dict[str, Any]]:
    final = []
    for rp_doc, matches, distances, hevy_ids in zip(
        rp_docs,
        results["documents"],
        results["distances"],
        results["ids"],
        strict=True,
    ):
        final.append(
            {
                "rp_id": rp_doc["id"],
                "rp_embedding_name": rp_doc["name"],
                "semantic_matches": [
                    {
                        "hevy_id": hid,
                        "hevy_embedding_name": m,
                        "distance": round(d, 2),
                    }
                    for hid, m, d in zip(hevy_ids, matches, distances, strict=True)
                ],
            }
        )
    return final


def _load_ground_truths(ground_truths_dir: str) -> dict[str, dict[str, str]]:
    """Load ground truth YAML files into a dict keyed by rp_exercise name."""
    import glob

    import yaml

    truths: dict[str, dict[str, str]] = {}
    for path in glob.glob(os.path.join(ground_truths_dir, "*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
        if data and "rp_exercise" in data and "best_match" in data:
            truths[data["rp_exercise"]] = data
    return truths


def _gt_matches(hevy_name: str, best_match: str) -> bool:
    """Check if a hevy embedding name matches the ground truth best_match.

    Ground truths may store a prefix (e.g. "shrug barbell") while the full
    hevy name includes muscle groups (e.g. "shrug barbell, traps, neck").
    """
    return hevy_name == best_match or hevy_name.startswith(best_match + ",")


def _confidence_weight(confidence: str) -> float:
    if confidence == "high":
        return 1.0
    if confidence == "medium":
        return 0.5
    return 0.0


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
    ground_truths_dir: str | None = None,
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

    metrics: dict[str, Any] = {
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

    # Ground truth accuracy (when ground truth files are available)
    if ground_truths_dir:
        gt = _load_ground_truths(ground_truths_dir)
        if gt:
            metrics["ground_truth"] = _compute_ground_truth_metrics(
                rp_docs, results, gt
            )

    return metrics


def _compute_ground_truth_metrics(
    rp_docs: list[str],
    results: chromadb.QueryResult,
    gt: dict[str, dict[str, str]],
) -> dict[str, Any]:
    top1_score = 0.0
    topk_score = 0.0
    none_correct_score = 0.0
    evaluated = 0
    none_total = 0
    mismatches: list[dict[str, str]] = []

    for rp_doc, matches in zip(rp_docs, results["documents"], strict=True):
        if rp_doc not in gt:
            continue

        truth = gt[rp_doc]
        best_match = truth["best_match"]
        weight = _confidence_weight(truth.get("confidence", "high"))
        evaluated += 1

        if best_match == "none":
            # Ground truth says none of the candidates match — any top-k
            # result that ISN'T in the candidate list is fine, but if the
            # embedding returns a candidate that was explicitly rejected,
            # that's a miss.  For "none" truths we just track them separately.
            none_total += 1
            none_correct_score += weight
            continue

        # Check top-1
        if _gt_matches(matches[0], best_match):
            top1_score += weight
        else:
            mismatches.append(
                {
                    "rp_exercise": rp_doc,
                    "expected": best_match,
                    "got": matches[0],
                    "confidence": truth.get("confidence", "high"),
                }
            )

        # Check top-k
        if any(_gt_matches(m, best_match) for m in matches):
            topk_score += weight

    n_matchable = evaluated - none_total
    return {
        "evaluated": evaluated,
        "matchable": n_matchable,
        "none_total": none_total,
        "weighted_accuracy_at_1": round(top1_score / n_matchable, 4)
        if n_matchable
        else 0,
        "weighted_accuracy_at_k": round(topk_score / n_matchable, 4)
        if n_matchable
        else 0,
        "weighted_top1_correct": round(top1_score, 2),
        "weighted_topk_correct": round(topk_score, 2),
        "mismatches": mismatches,
    }
