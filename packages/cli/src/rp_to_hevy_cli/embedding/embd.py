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

from rp_to_hevy_cli.embedding.utils import _data_options, _resolve_input
from rp_to_hevy_cli.settings import chroma_config, embedding_api_config


@click.command()
@_data_options
@click.option("--rp-prompt", default="", help="Prompt prepended to RP exercise texts.")
@click.option(
    "--hevy-prompt", default="", help="Prompt prepended to Hevy exercise texts."
)
def embd(
    rp_path: str,
    hevy_path: str,
    mappings_path: str,
    rp_prompt: str,
    hevy_prompt: str,
):
    """Embed exercises into ChromaDB."""
    base_url, api_key, model, dimensions, batch_size = embedding_api_config()
    embedder = ApiEmbedder(
        base_url=base_url,
        api_key=api_key,
        model=model,
        dimensions=dimensions,
        rate_limit=RateLimitConfig(batch_size=batch_size),
    )

    rp_raw = load_rp_exercises(_resolve_input(rp_path))
    hevy_raw = load_hevy_exercises(_resolve_input(hevy_path))
    mappings = load_muscle_group_mappings(_resolve_input(mappings_path))

    rp_df = prepare_rp_exercises(rp_raw, mappings)
    hevy_df = prepare_hevy_exercises(hevy_raw)

    chroma_host, chroma_port, chroma_api_key = chroma_config()
    client = create_client(
        host=chroma_host, port=chroma_port, api_key=chroma_api_key
    )
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
