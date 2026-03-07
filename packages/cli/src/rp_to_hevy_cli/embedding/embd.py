from __future__ import annotations

import click
from embeddings import (
    ApiEmbedder,
    RateLimitConfig,
    create_client,
    create_collection,
    encode_and_store,
    load_hevy_exercises,
    load_muscle_group_mappings,
    load_rp_exercises,
    prepare_hevy_exercises,
    prepare_rp_exercises,
)

from rp_to_hevy_cli.embedding.utils import (
    _chromadb_options,
    _data_options,
    _embedder_options,
    _resolve_input,
)


@click.command()
@_data_options
@_embedder_options
@_chromadb_options
@click.option("--rp-prompt", default="", help="Prompt prepended to RP exercise texts.")
@click.option(
    "--hevy-prompt", default="", help="Prompt prepended to Hevy exercise texts."
)
def embd(
    rp_path: str,
    hevy_path: str,
    mappings_path: str,
    api_base_url: str,
    api_key: str,
    api_model: str,
    api_dimensions: int | None,
    api_max_rpm: int,
    api_batch_size: int,
    chroma_host: str,
    chroma_port: int,
    rp_prompt: str,
    hevy_prompt: str,
):
    """Embed exercises into ChromaDB."""
    embedder = ApiEmbedder(
        base_url=api_base_url,
        api_key=api_key,
        model=api_model,
        dimensions=api_dimensions,
        rate_limit=RateLimitConfig(
            max_requests_per_minute=api_max_rpm,
            batch_size=api_batch_size,
        ),
    )

    rp_raw = load_rp_exercises(_resolve_input(rp_path))
    hevy_raw = load_hevy_exercises(_resolve_input(hevy_path))
    mappings = load_muscle_group_mappings(_resolve_input(mappings_path))

    rp_df = prepare_rp_exercises(rp_raw, mappings)
    hevy_df = prepare_hevy_exercises(hevy_raw)

    client = create_client(host=chroma_host, port=chroma_port)
    hevy_collection = create_collection(client, "hevy_exercises")
    rp_collection = create_collection(client, "rp_exercises")

    hevy_docs = hevy_df["rich_text_representation"].to_list()
    hevy_ids = hevy_df["hevy_id"].to_list()
    hevy_metadatas = [
        {"primary_muscle_group": mg}
        for mg in hevy_df["hevy_primary_muscle_group"].to_list()
    ]
    encode_and_store(
        embedder,
        hevy_collection,
        hevy_docs,
        hevy_ids,
        prompt=hevy_prompt,
        metadatas=hevy_metadatas,
    )

    rp_docs = rp_df["rich_text_representation"].to_list()
    rp_ids = rp_df["rp_id"].cast(str).to_list()
    encode_and_store(
        embedder,
        rp_collection,
        rp_docs,
        rp_ids,
        prompt=rp_prompt,
    )

    click.echo(
        f"Embedded {len(hevy_docs)} Hevy and {len(rp_docs)} RP exercises "
        f"into ChromaDB ({chroma_host}:{chroma_port})."
    )
