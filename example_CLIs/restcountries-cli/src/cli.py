#!/usr/bin/env python3
"""
restcountries-cli - Auto-generated CLI from PRD.md
"""

import click
from src.config import Config

from src.commands.countries_commands import countries_group


@click.group()
@click.option('--config', type=click.Path(exists=False), help='Config file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    Restcountries-Cli - API CLI Client

    API: REST Countries API Python Client - Product Requirements Document
    Version: 3.1
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config_path=config)
    ctx.obj['verbose'] = verbose


# Register resource commands
cli.add_command(countries_group, 'countries')


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
