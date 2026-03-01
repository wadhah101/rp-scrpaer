from __future__ import annotations

import click

from .embedding import embedding
from .hevy import hevy
from .rp import rp


@click.group()
def cli():
    """RP Hypertrophy to STRONG workout data exporter."""


cli.add_command(rp)
cli.add_command(hevy)
cli.add_command(embedding)

if __name__ == "__main__":
    cli()
