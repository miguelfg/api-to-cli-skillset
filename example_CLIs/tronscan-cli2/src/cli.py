"""Main Click CLI entry point for tronscan-cli."""

import sys
from typing import Optional

import click

from src.client import TronscanClient
from src.commands.accounts_commands import accounts
from src.commands.blocks_commands import blocks
from src.commands.contracts_commands import contracts
from src.config import Config
from src.logger import setup_logger


@click.group()
@click.version_option("1.0.0", prog_name="tronscan")
@click.option("--api-key", default=None, envvar="TRONSCAN_API_KEY", help="Tronscan API key (TRON-PRO-API-KEY).")
@click.option("--verbose", is_flag=True, default=False, help="Enable DEBUG-level output.")
@click.pass_context
def cli(ctx: click.Context, api_key: Optional[str], verbose: bool) -> None:
    """tronscan — TRON blockchain explorer CLI.

    Queries the Tronscan API (https://apilist.tronscanapi.com) for
    account, block, and contract data.

    \b
    Quick start:
      tronscan accounts list --limit 20
      tronscan blocks stats
      tronscan contracts list --search USDT
    """
    ctx.ensure_object(dict)

    setup_logger(verbose=verbose)

    effective_key = api_key or Config.API_KEY
    if not effective_key:
        click.echo(
            "Error: API key not configured.\n"
            "Use one of:\n"
            "  1. export TRONSCAN_API_KEY=your-key\n"
            "  2. Add TRONSCAN_API_KEY=your-key to .env\n"
            "  3. Pass --api-key your-key",
            err=True,
        )
        sys.exit(1)

    ctx.obj["client"] = TronscanClient(api_key=effective_key, verbose=verbose)


@cli.command("batch")
@click.option(
    "--input-file",
    required=True,
    type=click.Path(exists=True),
    help="TXT (JSON Lines) batch input file — one JSON object per line.",
)
@click.option("--output-dir", default=None, help="Output directory for results XLSX.")
@click.option("--dry-run", is_flag=True, help="Validate input without calling the API.")
@click.option("--verbose", is_flag=True, help="Enable debug output.")
@click.pass_context
def batch(
    ctx: click.Context,
    input_file: str,
    output_dir: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> None:
    """Process a TXT (JSON Lines) batch file and save results to XLSX.

    \b
    Input file format (one JSON object per line):
      {"command": "accounts-list", "limit": 20}
      {"command": "accounts-get", "address": "TAddr..."}
      {"command": "blocks-list", "limit": 10}
      {"command": "contracts-get", "contract": "TAddr..."}

    Supported commands:
      accounts-list, accounts-get, accounts-tokens,
      blocks-list, blocks-stats,
      contracts-list, contracts-get, contracts-events
    """
    from src.batch_processor import process_batch

    out_dir = output_dir or Config.OUTPUT_DIR
    client: TronscanClient = ctx.obj["client"]

    try:
        path = process_batch(
            input_file=input_file,
            output_dir=out_dir,
            client=client,
            dry_run=dry_run,
        )
        if not dry_run:
            click.echo(f"Results saved → {path}")
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)


# Register resource sub-groups
cli.add_command(accounts)
cli.add_command(blocks)
cli.add_command(contracts)


def main() -> None:
    """Entry point for the tronscan CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
