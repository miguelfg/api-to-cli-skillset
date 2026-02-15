"""Transaction query commands for Tronscan API."""

import click
import json
import asyncio
import logging

logger = logging.getLogger(__name__)


@click.group()
def transactions():
    """Commands for querying TRON transactions."""
    pass


@transactions.command()
@click.option(
    "--hash",
    required=True,
    help="Transaction hash",
)
@click.pass_context
def info(ctx, hash: str):
    """Get transaction details by hash."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/transaction", params={"hash": hash})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@transactions.command()
@click.pass_context
def count(ctx):
    """Get total transaction count."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/transaction/count")

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@transactions.command()
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
    """List transactions (paginated)."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/transactionlist", params={"start": start, "limit": limit})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@transactions.command()
@click.pass_context
def stats(ctx):
    """Get transaction count statistics."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/transactioncount")

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
