from __future__ import annotations

import click

from rp_to_hevy_cli.embedding.embd import embd
from rp_to_hevy_cli.embedding.similarity_search import run_rp_similarity_search


@click.group()
def embedding():
    """Embedding and similarity search commands."""


embedding.add_command(embd)
embedding.add_command(run_rp_similarity_search)
