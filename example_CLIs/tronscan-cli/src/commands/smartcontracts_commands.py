"""Smart Contract query commands for Tronscan API."""

import click
import json
import asyncio


@click.group()
def smartcontracts():
    """Commands for querying smart contracts."""
    pass


@smartcontracts.command()
@click.option(
    "--address",
    required=True,
    help="Smart contract address",
)
@click.pass_context
def info(ctx, address: str):
    """Get smart contract information."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/contract", params={"address": address})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


@smartcontracts.command()
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
    """List smart contracts (paginated)."""
    client = ctx.obj["client"]

    async def fetch():
        return await client.get("/api/contractlist", params={"start": start, "limit": limit})

    try:
        result = asyncio.run(fetch())
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
