"""Account query commands for Tronscan API."""

import click
import json
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


@click.group()
def accounts():
    """Commands for querying TRON accounts."""
    pass


@accounts.command()
@click.option(
    "--address",
    required=True,
    help="TRON account address",
)
@click.option(
    "--format",
    type=click.Choice(["json", "xlsx"]),
    default="json",
    help="Output format",
)
@click.pass_context
def info(ctx, address: str, format: str):
    """Get account information by address."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/account", params={"address": address})

    try:
        result = asyncio.run(fetch())
        if format == "json":
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"Account info for {address}: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@accounts.command()
@click.option(
    "--address",
    required=True,
    help="TRON account address",
)
@click.pass_context
def votes(ctx, address: str):
    """Get voting information for an account."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get(f"/api/account/{address}/votes")

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@accounts.command()
@click.option(
    "--start",
    type=int,
    default=0,
    help="Starting index for pagination",
)
@click.option(
    "--limit",
    type=int,
    default=20,
    help="Number of results per page (max 200)",
)
@click.option(
    "--format",
    type=click.Choice(["json", "xlsx"]),
    default="json",
    help="Output format",
)
@click.pass_context
def list(ctx, start: int, limit: int, format: str):
    """List accounts (paginated)."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/accountlist", params={"start": start, "limit": limit})

    try:
        result = asyncio.run(fetch())
        if format == "json":
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"Retrieved {len(result.get('data', []))} accounts")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
