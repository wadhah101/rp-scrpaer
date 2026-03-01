from __future__ import annotations

import functools
import tempfile
from pathlib import Path

import click
import numpy as np
import yaml
from cloudpathlib import AnyPath, CloudPath
from embeddings import (
    ApiEmbedder,
    ClientMode,
    LocalEmbedder,
    RateLimitConfig,
    build_match_results,
    compute_metrics,
    create_client,
    create_collection,
    create_local_embedder,
    detect_device,
    encode_and_store,
    load_hevy_exercises,
    load_muscle_group_mappings,
    load_rp_exercises,
    prepare_hevy_exercises,
    prepare_rp_exercises,
    query_matches,
)
from embeddings.embed import DEFAULT_N_RESULTS

# ---------------------------------------------------------------------------
# Shared option decorators
# ---------------------------------------------------------------------------


def _data_options(f):
    @click.option(
        "--rp-path",
        default="data/rp/exercises.json",
        help="Path to RP exercises JSON.",
    )
    @click.option(
        "--hevy-path",
        default="data/hevy/exercises.json",
        help="Path to Hevy exercises JSON.",
    )
    @click.option(
        "--mappings-path",
        default="data/muscle_group_mapping.json",
        help="Path to muscle-group mapping JSON.",
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def _embedder_options(f):
    @click.option(
        "--backend",
        type=click.Choice(["local", "api"], case_sensitive=False),
        default="local",
        help="Embedding backend.",
    )
    @click.option(
        "--model-name", default="Qwen/Qwen3-Embedding-8B", help="Local model name."
    )
    @click.option(
        "--api-base-url", default=None, help="API base URL (required for api backend)."
    )
    @click.option("--api-key", default=None, help="API key (required for api backend).")
    @click.option(
        "--api-model", default=None, help="API model name (required for api backend)."
    )
    @click.option(
        "--api-dimensions", type=int, default=None, help="API embedding dimensions."
    )
    @click.option(
        "--api-max-rpm", type=int, default=60, help="API max requests per minute."
    )
    @click.option("--api-batch-size", type=int, default=100, help="API batch size.")
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def _chromadb_options(f):
    @click.option(
        "--chroma-mode",
        type=click.Choice(["memory", "persistent", "http"], case_sensitive=False),
        default="persistent",
        help="ChromaDB client mode.",
    )
    @click.option(
        "--chroma-path", default="./chroma_data", help="Path for persistent ChromaDB."
    )
    @click.option("--chroma-host", default="localhost", help="Host for HTTP ChromaDB.")
    @click.option(
        "--chroma-port", type=int, default=8000, help="Port for HTTP ChromaDB."
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def _common_options(f):
    f = _data_options(f)
    f = _embedder_options(f)
    f = _chromadb_options(f)
    return f


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_embedder(
    backend: str,
    model_name: str,
    api_base_url: str | None,
    api_key: str | None,
    api_model: str | None,
    api_dimensions: int | None,
    api_max_rpm: int,
    api_batch_size: int,
) -> ApiEmbedder | LocalEmbedder:
    if backend == "api":
        if not api_base_url or not api_key or not api_model:
            raise click.ClickException(
                "api_base_url, api_key, and api_model are required when backend='api'"
            )
        return ApiEmbedder(
            base_url=api_base_url,
            api_key=api_key,
            model=api_model,
            dimensions=api_dimensions,
            rate_limit=RateLimitConfig(
                max_requests_per_minute=api_max_rpm,
                batch_size=api_batch_size,
            ),
        )
    device = detect_device()
    return create_local_embedder(model_name, device)


def _build_chroma_client(
    chroma_mode: str,
    chroma_path: str,
    chroma_host: str,
    chroma_port: int,
):
    return create_client(
        mode=ClientMode(chroma_mode),
        path=chroma_path,
        host=chroma_host,
        port=chroma_port,
    )


def _resolve_input(path_str: str) -> str:
    """If *path_str* is a cloud URI, download to a local temp file and return its path."""
    path = AnyPath(path_str)
    if isinstance(path, CloudPath):
        suffix = "".join(path.suffixes)
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(path.read_bytes())
        tmp.close()
        return tmp.name
    return path_str


def _write_yaml(data: object, output_path: str) -> None:
    path = AnyPath(output_path)
    content = yaml.dump(data, sort_keys=False, default_flow_style=False)
    if isinstance(path, CloudPath):
        path.write_text(content)
    else:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content)
    click.echo(f"Wrote {path}")


# ---------------------------------------------------------------------------
# CLI group + commands
# ---------------------------------------------------------------------------


@click.group()
def embedding():
    """Embedding and similarity search commands."""


@embedding.command()
@_common_options
@click.option("--rp-prompt", default="", help="Prompt prepended to RP exercise texts.")
@click.option(
    "--hevy-prompt", default="", help="Prompt prepended to Hevy exercise texts."
)
def embd(
    rp_path: str,
    hevy_path: str,
    mappings_path: str,
    backend: str,
    model_name: str,
    api_base_url: str | None,
    api_key: str | None,
    api_model: str | None,
    api_dimensions: int | None,
    api_max_rpm: int,
    api_batch_size: int,
    chroma_mode: str,
    chroma_path: str,
    chroma_host: str,
    chroma_port: int,
    rp_prompt: str,
    hevy_prompt: str,
):
    """Embed exercises into ChromaDB."""
    embedder = _build_embedder(
        backend,
        model_name,
        api_base_url,
        api_key,
        api_model,
        api_dimensions,
        api_max_rpm,
        api_batch_size,
    )

    rp_raw = load_rp_exercises(_resolve_input(rp_path))
    hevy_raw = load_hevy_exercises(_resolve_input(hevy_path))
    mappings = load_muscle_group_mappings(_resolve_input(mappings_path))

    rp_df = prepare_rp_exercises(rp_raw, mappings)
    hevy_df = prepare_hevy_exercises(hevy_raw)

    client = _build_chroma_client(chroma_mode, chroma_path, chroma_host, chroma_port)
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
        f"into ChromaDB ({chroma_mode})."
    )


@embedding.command("run-rp-similarity-search")
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
    default=None,
    help="Directory to write per-exercise YAML (opt-in).",
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
):
    """Run similarity search on already-embedded exercises in ChromaDB."""
    client = _build_chroma_client(chroma_mode, chroma_path, chroma_host, chroma_port)
    hevy_collection = create_collection(client, "hevy_exercises")
    rp_collection = create_collection(client, "rp_exercises")

    rp_data = rp_collection.get(include=["embeddings", "documents"])
    rp_embeddings = np.array(rp_data["embeddings"], dtype=np.float32)
    rp_docs = rp_data["documents"]

    results = query_matches(hevy_collection, rp_embeddings, n_results)

    hevy_data = hevy_collection.get(include=["documents"])
    hevy_docs = hevy_data["documents"]
    click.echo(
        f"Queried {len(rp_docs)} RP exercises against {len(hevy_docs)} Hevy exercises."
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
            rp_docs=rp_docs,
            hevy_docs=hevy_docs,
            rp_expected_muscles=rp_expected_muscles,
            results=results,
        )
        _write_yaml(metrics, metrics_output)

    if exercise_output_dir:
        match_results = build_match_results(rp_docs, results)
        for item in match_results:
            normalized = (
                item["rp_embedding_name"]
                .replace(" ", "-")
                .replace(",", "")
                .replace("/", "")
                .replace(")", "")
                .replace("(", "")
            )
            _write_yaml(item, str(AnyPath(exercise_output_dir) / f"{normalized}.yaml"))
