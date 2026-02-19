"""Click commands for the Blocks resource."""

from typing import Optional

import click

from src.client import TronscanClient
from src.output import print_json, save_xlsx


@click.group()
def blocks() -> None:
    """TRON blockchain block data."""


@blocks.command("list")
@click.option("--start", default=0, show_default=True, help="Start index for pagination.")
@click.option("--limit", default=10, show_default=True, help="Items per page.")
@click.option("--producer", default=None, help="Filter by super representative address.")
@click.option("--sort", default="-number", show_default=True, help="Sort criteria.")
@click.option("--start-timestamp", default=None, type=int, help="Filter from Unix ms timestamp.")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def blocks_list(
    ctx: click.Context,
    start: int,
    limit: int,
    producer: Optional[str],
    sort: str,
    start_timestamp: Optional[int],
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """List TRON blocks with optional producer/timestamp filters."""
    params = {
        "start": start,
        "limit": limit,
        "producer": producer,
        "sort": sort,
        "start_timestamp": start_timestamp,
    }
    if dry_run:
        click.echo(f"DRY RUN  GET /api/block  params={params}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/block", params=params)
    if fmt == "xlsx":
        save_xlsx(data, stem="blocks_list", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)


@blocks.command("stats")
@click.option("--format", "fmt", type=click.Choice(["json", "xlsx"]), default="xlsx", show_default=True)
@click.option("--output-file", default=None, help="Explicit output file path.")
@click.option("--output-dir", default=None, help="Output directory (timestamped filename).")
@click.option("--dry-run", is_flag=True, help="Show request params without executing.")
@click.pass_context
def blocks_stats(
    ctx: click.Context,
    fmt: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    dry_run: bool,
) -> None:
    """Get block statistical summary (burn, count, last day pay)."""
    if dry_run:
        click.echo("DRY RUN  GET /api/block/statistic  params={}")
        return
    client: TronscanClient = ctx.obj["client"]
    data = client.get("/api/block/statistic")
    if fmt == "xlsx":
        save_xlsx(data, stem="block_stats", output_dir=output_dir, output_file=output_file)
    else:
        print_json(data)
