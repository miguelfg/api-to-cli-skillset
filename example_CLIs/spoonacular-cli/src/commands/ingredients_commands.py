"""
CLI commands for ingredients resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def ingredients_group(ctx):
    """Manage Ingredients resources."""
    ctx.obj = ctx.obj or {}


@ingredients_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.option('--query', type=str, help='Ingredient query')
@click.option('--number', type=int, default=10, show_default=True, help='Result limit')
@click.option('--offset', type=int, default=0, show_default=True, help='Pagination offset')
@click.option('--add-children', is_flag=True, help='Include child ingredient matches')
@click.option('--meta-information', is_flag=True, help='Include extra ingredient metadata')
@click.pass_context
def list(ctx, format, query, number, offset, add_children, meta_information):
    """List all ingredients."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get(
            '/food/ingredients/search',
            params={
                'query': query,
                'number': number,
                'offset': offset,
                'addChildren': add_children,
                'metaInformation': meta_information,
            },
        )
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@ingredients_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a ingredient by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get(f'/food/ingredients/{id}/information')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@ingredients_group.command()
@click.option('--data', type=str, help='JSON data for the ingredient')
@click.pass_context
def create(ctx, data):
    """Ingredient creation is not part of this generated Spoonacular subset."""
    raise click.ClickException('Create is not implemented for the read-focused Spoonacular subset.')
