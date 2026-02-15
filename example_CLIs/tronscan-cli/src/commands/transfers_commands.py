"""Token Transfer query commands for Tronscan API."""

import click
import json
import asyncio


@click.group()
def transfers():
    """Commands for querying token transfers."""
    pass


@transfers.command()
@click.option(
    "--hash",
    required=True,
    help="Transfer hash",
)
@click.pass_context
def info(ctx, hash: str):
    """Get token transfer information."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/transfer", params={"hash": hash})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@transfers.command()
@click.option(
    "--start",
    type=int,
    default=0,
    help="Starting index",
)
@click.option(
    "--limit",
    type=int,
    default=20,
    help="Results per page",
)
@click.pass_context
def list(ctx, start: int, limit: int):
    """List token transfers (paginated)."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/transferlist", params={"start": start, "limit": limit})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
