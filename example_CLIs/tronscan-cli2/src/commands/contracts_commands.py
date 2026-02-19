"""Click commands for the Contracts resource."""

from typing import List, Optional

import click

from src.client import TronscanClient
from src.output import print_json, save_xlsx


@click.group()
def contracts() -> None:
    """TRON smart contract operations."""


@contracts.command("list")
@click.option("--search", default=None, help="Search term for contract name or address.")
@click.option("--start", default=0, show_default=True, help="Start index for pagination.")
@click.option("--limit", default=10, show_default=True, help="Items per page.")
@click.option("--sort", default=None, help="Sort criteria.")
@click.option("--open-source-only/--all", default=False, help="Filter to open-source contracts only.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def contracts_list(
    ctx: click.Context,
    search: Optional[str],
    start: int,
    limit: int,
    sort: Optional[str],
    open_source_only: bool,
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """List smart contracts with optional search and filter."""
    params = {
        "search": search,
        "start": start,
        "limit": limit,
        "sort": sort,
        "open-source-only": open_source_only or None,
    }
    if dry_run:
        click.echo(f"DRY RUN  GET /api/contracts  params={params}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/contracts", params=params)
    if fmt == "xlsx":
        save_xlsx(data, stem="contracts_list", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)


@contracts.command("get")
@click.option("--contract", required=True, help="Contract address.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def contracts_get(
    ctx: click.Context,
    contract: str,
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """Get comprehensive details for a specific smart contract."""
    if dry_run:
        click.echo(f"DRY RUN  GET /api/contract  params={{contract={contract!r}}}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/contract", params={"contract": contract})
    if fmt == "xlsx":
        save_xlsx(data, stem="contract_details", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)


@contracts.command("events")
@click.option("--contract-address", default=None, help="Contract address filter.")
@click.option("--hash", "hashes", multiple=True, help="Transaction hash(es) to filter by.")
@click.option("--term", default=None, help="Search term (e.g. Transfer).")
@click.option("--limit", default=20, show_default=True, help="Number of events to return.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request body without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def contracts_events(
    ctx: click.Context,
    contract_address: Optional[str],
    hashes: tuple,
    term: Optional[str],
    limit: int,
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """Get event logs for a contract (batch endpoint)."""
    body = {
        "contractAddress": contract_address,
        "hashList": list(hashes),
        "term": term,
        "limit": limit,
    }
    if dry_run:
        click.echo(f"DRY RUN  POST /api/contracts/smart-contract-triggers-batch  body={body}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.post("/api/contracts/smart-contract-triggers-batch", json=body)
    if fmt == "xlsx":
        save_xlsx(data, stem="contract_events", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)
