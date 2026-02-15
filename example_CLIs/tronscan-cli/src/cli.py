"""Tronscan API CLI - Main entry point."""

import click
import logging
import asyncio
from pathlib import Path

from .config import Config, setup_logging
from .client import TronscanClient
from .batch_processor import BatchProcessor
from .commands.accounts_commands import accounts
from .commands.transactions_commands import transactions
from .commands.blocks_commands import blocks
from .commands.smartcontracts_commands import smartcontracts
from .commands.transfers_commands import transfers
from .commands.tokens_commands import tokens
from .commands.network_commands import network


class Config:
    """CLI context configuration."""

    def __init__(self, env_file: str = ".env"):
        self.config = Config(env_file)
        self.client = TronscanClient(
            base_url=self.config.base_url,
            api_key=self.config.api_key,
            timeout=self.config.timeout,
            max_retries=self.config.retries,
            retry_delay=self.config.retry_delay,
        )
        setup_logging(self.config.log_level)


@click.group()
@click.option(
    "--env-file",
    type=click.Path(),
    default=".env",
    help="Path to .env configuration file",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable debug logging",
)
@click.pass_context
def cli(ctx, env_file: str, verbose: bool):
    """Tronscan API Python CLI Client.

    Query TRON blockchain data including accounts, transactions, blocks,
    smart contracts, tokens, and network information.
    """
    config = Config(env_file)

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    ctx.ensure_object(dict)
    ctx.obj["client"] = config.client
    ctx.obj["batch_processor"] = BatchProcessor(config.client)


# Add resource groups
cli.add_command(accounts)
cli.add_command(transactions)
cli.add_command(blocks)
cli.add_command(smartcontracts)
cli.add_command(transfers)
cli.add_command(tokens)
cli.add_command(network)


@cli.command()
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    required=True,
    help="CSV batch input file",
)
@click.option(
    "--format",
    type=click.Choice(["json", "xlsx"]),
    default="json",
    help="Output format",
)
@click.option(
    "--output-path",
    type=click.Path(),
    default="output",
    help="Output directory path",
)
@click.option(
    "--include-timestamp",
    is_flag=True,
    default=True,
    help="Include timestamp in output filename",
)
@click.pass_context
def batch(ctx, input_file: str, format: str, output_path: str, include_timestamp: bool):
    """Process batch requests from CSV file.

    CSV format:
    method,endpoint,param1,param2
    GET,/api/account,address
    GET,/api/transaction,hash
    """
    processor = ctx.obj.get("batch_processor")

    if not processor:
        click.echo("Error: Batch processor not initialized", err=True)
        raise click.Exit(1)

    try:
        # Update output directory
        processor.output_dir = Path(output_path)

        # Process batch
        output_file = asyncio.run(
            processor.process_csv(
                input_file,
                format=format,
                include_timestamp=include_timestamp,
            )
        )

        click.echo(f"✅ Batch processed successfully")
        click.echo(f"📁 Results saved to: {output_file}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)
    except Exception as e:
        click.echo(f"Error processing batch: {e}", err=True)
        raise click.Exit(1)


@cli.command()
@click.pass_context
def config(ctx):
    """Show current configuration."""
    client = ctx.obj.get("client")

    if not client:
        click.echo("Error: Client not initialized", err=True)
        raise click.Exit(1)

    click.echo("Tronscan CLI Configuration:")
    click.echo(f"  Base URL: {client.base_url}")
    click.echo(f"  Timeout: {client.timeout}s")
    click.echo(f"  Max Retries: {client.max_retries}")
    click.echo(f"  Retry Delay: {client.retry_delay}s")


if __name__ == "__main__":
    cli()
