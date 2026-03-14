"""
CLI commands for recipes resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def recipes_group(ctx):
    """Manage Recipes resources."""
    ctx.obj = ctx.obj or {}


@recipes_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.option('--query', type=str, help='Natural-language recipe query')
@click.option('--diet', type=str, help='Diet filter')
@click.option('--cuisine', type=str, help='Cuisine filter')
@click.option('--number', type=int, default=10, show_default=True, help='Result limit')
@click.option('--offset', type=int, default=0, show_default=True, help='Pagination offset')
@click.pass_context
def list(ctx, format, query, diet, cuisine, number, offset):
    """List all recipes."""
    client = APIClient(ctx.obj['config'])
    try:
        params = {
            'query': query,
            'diet': diet,
            'cuisine': cuisine,
            'number': number,
            'offset': offset,
        }
        results = client.get(
            '/recipes/complexSearch',
            params={k: v for k, v in params.items() if v is not None},
        )
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@recipes_group.command()
@click.argument('id')
@click.option('--include-nutrition', is_flag=True, help='Include nutrition data')
@click.option('--add-wine-pairing', is_flag=True, help='Include wine pairing')
@click.option('--add-taste-data', is_flag=True, help='Include taste data')
@click.pass_context
def get(ctx, id, include_nutrition, add_wine_pairing, add_taste_data):
    """Get a recipe by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get(
            f'/recipes/{id}/information',
            params={
                'includeNutrition': include_nutrition,
                'addWinePairing': add_wine_pairing,
                'addTasteData': add_taste_data,
            },
        )
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@recipes_group.command()
@click.option('--data', type=str, help='JSON data for the recipe')
@click.pass_context
def create(ctx, data):
    """Recipe creation is not part of this generated Spoonacular subset."""
    raise click.ClickException('Create is not implemented for the read-focused Spoonacular subset.')
