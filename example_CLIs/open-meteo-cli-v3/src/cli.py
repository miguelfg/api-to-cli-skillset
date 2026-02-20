#!/usr/bin/env python3
"""
open-meteo-cli-v3 - Auto-generated CLI from PRD.md
"""

import click
from src.config import Config

from src.commands.overview_commands import overview_group
from src.commands.purpose_commands import purpose_group
from src.commands.requirements_commands import requirements_group
from src.commands.setup_commands import setup_group
from src.commands.verify_commands import verify_group
from src.commands.method_commands import method_group
from src.commands.strategy_commands import strategy_group


@click.group()
@click.option('--config', type=click.Path(exists=False), help='Config file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    Open-Meteo-Cli-V3 - API CLI Client

    API: open-meteo Python Client - Product Requirements Document
    Version: 1.0
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config_path=config)
    ctx.obj['verbose'] = verbose


# Register resource commands
cli.add_command(overview_group, 'overview')
cli.add_command(purpose_group, 'purpose')
cli.add_command(requirements_group, 'requirements')
cli.add_command(setup_group, 'setup')
cli.add_command(verify_group, 'verify')
cli.add_command(method_group, 'method')
cli.add_command(strategy_group, 'strategy')


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
