"""
CLI commands for products resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def products_group(ctx):
    """Manage Products resources."""
    ctx.obj = ctx.obj or {}


@products_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.option('--query', type=str, help='Product query')
@click.option('--number', type=int, default=10, show_default=True, help='Result limit')
@click.option('--offset', type=int, default=0, show_default=True, help='Pagination offset')
@click.option('--add-product-information', is_flag=True, help='Include expanded product fields')
@click.pass_context
def list(ctx, format, query, number, offset, add_product_information):
    """List all products."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get(
            '/food/products/search',
            params={
                'query': query,
                'number': number,
                'offset': offset,
                'addProductInformation': add_product_information,
            },
        )
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@products_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a product by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get(f'/food/products/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@products_group.command()
@click.option('--data', type=str, help='JSON data for the product')
@click.pass_context
def create(ctx, data):
    """Product creation is not part of this generated Spoonacular subset."""
    raise click.ClickException('Create is not implemented for the read-focused Spoonacular subset.')
