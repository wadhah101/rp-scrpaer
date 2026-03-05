from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from embeddings import (
    build_match_results,
    compute_metrics,
    create_collection,
    load_muscle_group_mappings,
    load_rp_exercises,
    prepare_rp_exercises,
    query_matches,
)
from embeddings.embed import DEFAULT_N_RESULTS

from rp_to_hevy_cli.embedding.utils import (
    _build_chroma_client,
    _chromadb_options,
    _resolve_input,
    _write_yaml,
)


@click.command("run-rp-similarity-search")
@_chromadb_options
@click.option(
    "--n-results",
    type=int,
    default=DEFAULT_N_RESULTS,
    help="Number of results per query.",
)
@click.option(
    "--metrics-output", default=None, help="Path to write metrics YAML (opt-in)."
)
@click.option(
    "--exercise-output-dir",
    default="data/embeddings/output",
    help="Directory to write per-exercise YAML.",
)
@click.option(
    "--rp-path",
    default="data/rp/exercises.json",
    help="Path to RP exercises JSON (used for metrics ground truth).",
)
@click.option(
    "--mappings-path",
    default="data/muscle_group_mapping.json",
    help="Path to muscle-group mapping JSON (used for metrics ground truth).",
)
@click.option("--model-name", default="", help="Model name label for metrics output.")
@click.option("--rp-prompt", default="", help="RP prompt label for metrics output.")
@click.option("--hevy-prompt", default="", help="Hevy prompt label for metrics output.")
@click.option(
    "--ground-truths-dir",
    default="data/embeddings/ground-truths",
    help="Directory containing ground truth YAML files.",
)
def run_rp_similarity_search(
    chroma_mode: str,
    chroma_path: str,
    chroma_host: str,
    chroma_port: int,
    n_results: int,
    metrics_output: str | None,
    exercise_output_dir: str | None,
    rp_path: str,
    mappings_path: str,
    model_name: str,
    rp_prompt: str,
    hevy_prompt: str,
    ground_truths_dir: str,
):
    """Run similarity search on already-embedded exercises in ChromaDB."""
    client = _build_chroma_client(chroma_mode, chroma_path, chroma_host, chroma_port)
    hevy_collection = create_collection(client, "hevy_exercises")
    rp_collection = create_collection(client, "rp_exercises")

    rp_data = rp_collection.get(include=["embeddings", "documents"])
    rp_embeddings = np.array(rp_data["embeddings"], dtype=np.float32)
    rp_ids = rp_data["ids"]
    rp_doc_names = rp_data["documents"] or []
    rp_docs = [{"id": id_, "name": name} for id_, name in zip(rp_ids, rp_doc_names)]

    results = query_matches(hevy_collection, rp_embeddings, n_results)

    hevy_data = hevy_collection.get(include=["documents"])
    hevy_docs = hevy_data["documents"] or []
    click.echo(
        f"Queried {len(rp_doc_names)} RP exercises against {len(hevy_docs)} Hevy exercises."
    )

    if metrics_output:
        rp_raw = load_rp_exercises(_resolve_input(rp_path))
        mappings = load_muscle_group_mappings(_resolve_input(mappings_path))
        rp_df = prepare_rp_exercises(rp_raw, mappings)
        rp_expected_muscles = rp_df["hevy_primary"].to_list()
        metrics = compute_metrics(
            model_name=model_name,
            rp_prompt=rp_prompt,
            hevy_prompt=hevy_prompt,
            n_results=n_results,
            device="",
            rp_docs=rp_doc_names,
            hevy_docs=hevy_docs,
            rp_expected_muscles=rp_expected_muscles,
            results=results,
            ground_truths_dir=ground_truths_dir,
        )
        _write_yaml(metrics, metrics_output)

    if exercise_output_dir:
        match_results = build_match_results(rp_docs, results)
        for item in match_results:
            normalized = (
                item["rp_id"]
                .replace(" ", "-")
                .replace(",", "")
                .replace("/", "")
                .replace(")", "")
                .replace("(", "")
            )
            _write_yaml(item, str(Path(exercise_output_dir) / f"{normalized}.yaml"))
