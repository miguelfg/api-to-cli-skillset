"""Block query commands for Tronscan API."""

import click
import json
import asyncio


@click.group()
def blocks():
    """Commands for querying TRON blocks."""
    pass


@blocks.command()
@click.option(
    "--number",
    type=int,
    required=True,
    help="Block number",
)
@click.pass_context
def info(ctx, number: int):
    """Get block information by number."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/block", params={"number": number})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@blocks.command()
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
    """List blocks (paginated)."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/blocklist", params={"start": start, "limit": limit})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@blocks.command()
@click.pass_context
def count(ctx):
    """Get total block count."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/blockcount")

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
