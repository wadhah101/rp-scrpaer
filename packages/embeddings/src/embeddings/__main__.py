import logging
import os

import yaml

from embeddings.db import create_client, create_collection
from embeddings.df import (
    load_hevy_exercises,
    load_muscle_group_mappings,
    load_rp_exercises,
    prepare_hevy_exercises,
    prepare_rp_exercises,
)
from embeddings.embed import (
    DEFAULT_N_RESULTS,
    build_match_results,
    compute_metrics,
    detect_device,
    encode_and_store,
    load_model,
    query_matches,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main(
    *,
    model_name: str = "Qwen/Qwen3-Embedding-8B",
    rp_prompt: str = "",
    hevy_prompt: str = "",
    n_results: int = DEFAULT_N_RESULTS,
    rp_path: str = "data/rp/exercises.json",
    hevy_path: str = "data/hevy/exercises.json",
    mappings_path: str = "data/muscle_group_mapping.json",
    metrics_path: str = "metrics.yaml",
) -> None:
    device = detect_device()

    # Load and prepare data
    rp_raw = load_rp_exercises(rp_path)
    hevy_raw = load_hevy_exercises(hevy_path)
    mappings = load_muscle_group_mappings(mappings_path)

    rp_df = prepare_rp_exercises(rp_raw, mappings)
    hevy_df = prepare_hevy_exercises(hevy_raw)

    # Set up ChromaDB
    client = create_client()
    hevy_collection = create_collection(client, "hevy_exercises")
    rp_collection = create_collection(client, "rp_exercises")

    # Load model
    model = load_model(model_name, device)

    # Encode and store hevy exercises
    hevy_docs = hevy_df["rich_text_representation"].to_list()
    hevy_ids = hevy_df["hevy_id"].to_list()
    hevy_metadatas = [
        {"primary_muscle_group": mg}
        for mg in hevy_df["hevy_primary_muscle_group"].to_list()
    ]
    encode_and_store(
        model,
        hevy_collection,
        hevy_docs,
        hevy_ids,
        prompt=hevy_prompt,
        metadatas=hevy_metadatas,
    )

    # Encode and store rp exercises
    rp_docs = rp_df["rich_text_representation"].to_list()
    rp_ids = rp_df["rp_id"].cast(str).to_list()
    rp_embeddings = encode_and_store(
        model,
        rp_collection,
        rp_docs,
        rp_ids,
        prompt=rp_prompt,
    )

    # Query matches
    results = query_matches(hevy_collection, rp_embeddings, n_results)

    # Compute and write metrics
    rp_expected_muscles = rp_df["hevy_primary"].to_list()
    metrics = compute_metrics(
        model_name=model_name,
        rp_prompt=rp_prompt,
        hevy_prompt=hevy_prompt,
        n_results=n_results,
        device=device,
        rp_docs=rp_docs,
        hevy_docs=hevy_docs,
        rp_expected_muscles=rp_expected_muscles,
        results=results,
    )

    with open(metrics_path, "w") as f:
        yaml.dump(metrics, f, sort_keys=False, default_flow_style=False)
    logger.info("Metrics written to %s", metrics_path)

    # Optionally write per-exercise output
    monorepo_root = os.environ.get("MONOREPO_ROOT")
    update_output = os.environ.get("UPDATE_OUTPUT", "false").lower() == "true"

    if not update_output:
        logger.info("Skipping output update (set UPDATE_OUTPUT=true to enable)")
        return

    match_results = build_match_results(rp_docs, results)
    output_dir = f"{monorepo_root}/packages/embeddings/output"
    os.makedirs(output_dir, exist_ok=True)

    for item in match_results:
        normalized = (
            item["rp_embedding_name"]
            .replace(" ", "-")
            .replace(",", "")
            .replace("/", "")
            .replace(")", "")
            .replace("(", "")
        )
        with open(f"{output_dir}/{normalized}.yaml", "w") as f:
            yaml.dump(item, f, sort_keys=False)

    logger.info("Output written to %s", output_dir)


if __name__ == "__main__":
    main()
