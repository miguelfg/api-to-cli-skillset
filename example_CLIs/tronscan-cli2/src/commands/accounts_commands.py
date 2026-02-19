"""Click commands for the Accounts resource."""

from typing import Optional

import click

from src.client import TronscanClient
from src.output import print_json, save_xlsx


@click.group()
def accounts() -> None:
    """TRON account operations."""


@accounts.command("list")
@click.option("--start", default=0, show_default=True, help="Start index for pagination.")
@click.option("--limit", default=10, show_default=True, help="Items per page.")
@click.option("--sort", default=None, help="Sort criteria, e.g. -balance.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def accounts_list(
    ctx: click.Context,
    start: int,
    limit: int,
    sort: Optional[str],
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """List TRON accounts with pagination."""
    params = {"start": start, "limit": limit, "sort": sort}
    if dry_run:
        click.echo(f"DRY RUN  GET /api/account/list  params={params}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/account/list", params=params)
    if fmt == "xlsx":
        save_xlsx(data, stem="accounts_list", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)


@accounts.command("get")
@click.option("--address", required=True, help="TRON account address.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def accounts_get(
    ctx: click.Context,
    address: str,
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """Get comprehensive account details."""
    if dry_run:
        click.echo(f"DRY RUN  GET /api/accountv2  params={{address={address!r}}}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/accountv2", params={"address": address})
    if fmt == "xlsx":
        save_xlsx(data, stem="account_details", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)


@accounts.command("tokens")
@click.option("--address", required=True, help="TRON account address.")
@click.option("--start", default=0, show_default=True, help="Start index for pagination.")
@click.option("--limit", default=10, show_default=True, help="Items per page.")
@click.option("--hidden/--no-hidden", default=False, help="Include hidden tokens.")
@click.option("--sort-by", default=None, help="Sort field name, e.g. balance.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def accounts_tokens(
    ctx: click.Context,
    address: str,
    start: int,
    limit: int,
    hidden: bool,
    sort_by: Optional[str],
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """List tokens held by an account."""
    params = {
        "address": address,
        "start": start,
        "limit": limit,
        "hidden": hidden,
        "sortBy": sort_by,
    }
    if dry_run:
        click.echo(f"DRY RUN  GET /api/account/tokens  params={params}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/account/tokens", params=params)
    if fmt == "xlsx":
        save_xlsx(data, stem="account_tokens", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)
