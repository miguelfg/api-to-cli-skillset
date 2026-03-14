#!/usr/bin/env python3
"""
spoonacular-cli - Auto-generated CLI from PRD.md
"""

import click
from src.config import Config

from src.commands.recipes_commands import recipes_group
from src.commands.ingredients_commands import ingredients_group
from src.commands.products_commands import products_group
from src.commands.menuitems_commands import menuitems_group
from src.commands.mealplanner_commands import mealplanner_group


@click.group()
@click.option('--config', type=click.Path(exists=False), help='Config file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    Spoonacular-Cli - API CLI Client

    API: Spoonacular Food API Python Client - Product Requirements Document
    Version: 1.0.0
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config_path=config)
    ctx.obj['verbose'] = verbose


# Register resource commands
cli.add_command(recipes_group, 'recipes')
cli.add_command(ingredients_group, 'ingredients')
cli.add_command(products_group, 'products')
cli.add_command(menuitems_group, 'menuitems')
cli.add_command(mealplanner_group, 'mealplanner')


@cli.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx', 'sqlite']), default='json')
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
