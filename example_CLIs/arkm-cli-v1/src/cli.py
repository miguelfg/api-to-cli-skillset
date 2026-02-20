#!/usr/bin/env python3
"""
arkm-cli-v1 - Auto-generated CLI from PRD.md
"""

import click
from src.config import Config

from src.commands.arkm_commands import arkm_group
from src.commands.balances_commands import balances_group
from src.commands.chains_commands import chains_group
from src.commands.cluster_commands import cluster_group
from src.commands.counterparties_commands import counterparties_group
from src.commands.flow_commands import flow_group
from src.commands.history_commands import history_group
from src.commands.intelligence_commands import intelligence_group
from src.commands.loans_commands import loans_group
from src.commands.marketdata_commands import marketdata_group
from src.commands.networks_commands import networks_group
from src.commands.portfolio_commands import portfolio_group
from src.commands.swaps_commands import swaps_group
from src.commands.tag_commands import tag_group
from src.commands.token_commands import token_group
from src.commands.transfers_commands import transfers_group
from src.commands.tx_commands import tx_group
from src.commands.user_commands import user_group
from src.commands.volume_commands import volume_group
from src.commands.ws_commands import ws_group


@click.group()
@click.option('--config', type=click.Path(exists=False), help='Config file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    Arkm-Cli-V1 - API CLI Client

    API: PRD: Arkham Intel API Python CLI Client
    Version: 1.1.0
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config_path=config)
    ctx.obj['verbose'] = verbose


# Register resource commands
cli.add_command(arkm_group, 'arkm')
cli.add_command(balances_group, 'balances')
cli.add_command(chains_group, 'chains')
cli.add_command(cluster_group, 'cluster')
cli.add_command(counterparties_group, 'counterparties')
cli.add_command(flow_group, 'flow')
cli.add_command(history_group, 'history')
cli.add_command(intelligence_group, 'intelligence')
cli.add_command(loans_group, 'loans')
cli.add_command(marketdata_group, 'marketdata')
cli.add_command(networks_group, 'networks')
cli.add_command(portfolio_group, 'portfolio')
cli.add_command(swaps_group, 'swaps')
cli.add_command(tag_group, 'tag')
cli.add_command(token_group, 'token')
cli.add_command(transfers_group, 'transfers')
cli.add_command(tx_group, 'tx')
cli.add_command(user_group, 'user')
cli.add_command(volume_group, 'volume')
cli.add_command(ws_group, 'ws')


@cli.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.option('--input-file', type=click.Path(exists=True), help='Batch input file (CSV/TXT)')
@click.option('--output-path', type=click.Path(), default='./output', help='Output directory')
@click.option('--include-timestamp', is_flag=True, help='Include timestamp in output filename')
@click.pass_context
def batch(ctx, format, input_file, output_path, include_timestamp):
    """Process batch requests from input file."""
    from src.batch_processor import BatchProcessor

    processor = BatchProcessor(
        config=ctx.obj['config'],
        output_format=format,
        output_path=output_path,
        include_timestamp=include_timestamp,
        timestamp_format=ctx.obj['config'].get('timestamp_format', '%Y%m%d_%H%M%S'),
    )
    processor.process_file(input_file)


if __name__ == '__main__':
    cli(obj={})
