"""Token query commands for Tronscan API."""

import click
import json
import asyncio


@click.group()
def tokens():
    """Commands for querying tokens."""
    pass


@tokens.command()
@click.option(
    "--address",
    required=True,
    help="Token contract address",
)
@click.pass_context
def info(ctx, address: str):
    """Get token information."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/token", params={"address": address})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@tokens.command()
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
    """List tokens (paginated)."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/tokenlist", params={"start": start, "limit": limit})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
