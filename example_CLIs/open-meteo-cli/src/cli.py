#!/usr/bin/env python3
"""
open-meteo-cli - Auto-generated CLI from PRD.md
"""

import click
from src.config import Config

from src.commands.airquality_commands import airquality_group
from src.commands.archive_commands import archive_group
from src.commands.bom_commands import bom_group
from src.commands.climate_commands import climate_group
from src.commands.cma_commands import cma_group
from src.commands.dmi_commands import dmi_group
from src.commands.dwdicon_commands import dwdicon_group
from src.commands.ecmwf_commands import ecmwf_group
from src.commands.elevation_commands import elevation_group
from src.commands.ensemble_commands import ensemble_group
from src.commands.flood_commands import flood_group
from src.commands.forecast_commands import forecast_group
from src.commands.gem_commands import gem_group
from src.commands.gfs_commands import gfs_group
from src.commands.jma_commands import jma_group
from src.commands.knmi_commands import knmi_group
from src.commands.marine_commands import marine_group
from src.commands.meteofrance_commands import meteofrance_group
from src.commands.metno_commands import metno_group
from src.commands.search_commands import search_group


@click.group()
@click.option('--config', type=click.Path(exists=False), help='Config file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    Open-Meteo-Cli - API CLI Client

    API: Open-Meteo API Python Client - Product Requirements Document
    Version: 1.0.0
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config_path=config)
    ctx.obj['verbose'] = verbose


# Register resource commands
cli.add_command(airquality_group, 'airquality')
cli.add_command(archive_group, 'archive')
cli.add_command(bom_group, 'bom')
cli.add_command(climate_group, 'climate')
cli.add_command(cma_group, 'cma')
cli.add_command(dmi_group, 'dmi')
cli.add_command(dwdicon_group, 'dwdicon')
cli.add_command(ecmwf_group, 'ecmwf')
cli.add_command(elevation_group, 'elevation')
cli.add_command(ensemble_group, 'ensemble')
cli.add_command(flood_group, 'flood')
cli.add_command(forecast_group, 'forecast')
cli.add_command(gem_group, 'gem')
cli.add_command(gfs_group, 'gfs')
cli.add_command(jma_group, 'jma')
cli.add_command(knmi_group, 'knmi')
cli.add_command(marine_group, 'marine')
cli.add_command(meteofrance_group, 'meteofrance')
cli.add_command(metno_group, 'metno')
cli.add_command(search_group, 'search')


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
