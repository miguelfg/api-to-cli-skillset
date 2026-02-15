"""Network/Chain query commands for Tronscan API."""

import click
import json
import asyncio


@click.group()
def network():
    """Commands for querying network and blockchain information."""
    pass


@network.command()
@click.pass_context
def parameters(ctx):
    """Get blockchain network parameters."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/chain/parameters")

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@network.command()
@click.pass_context
def stats(ctx):
    """Get blockchain statistics."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/chain/stat")

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
