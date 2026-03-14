"""
CLI commands for menuitems resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def menuitems_group(ctx):
    """Manage Menuitems resources."""
    ctx.obj = ctx.obj or {}


@menuitems_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.option('--query', type=str, help='Menu item query')
@click.option('--number', type=int, default=10, show_default=True, help='Result limit')
@click.option('--offset', type=int, default=0, show_default=True, help='Pagination offset')
@click.option('--add-menu-item-information', is_flag=True, help='Include expanded menu item fields')
@click.pass_context
def list(ctx, format, query, number, offset, add_menu_item_information):
    """List all menuitems."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get(
            '/food/menuItems/search',
            params={
                'query': query,
                'number': number,
                'offset': offset,
                'addMenuItemInformation': add_menu_item_information,
            },
        )
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@menuitems_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a menuitem by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get(f'/food/menuItems/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@menuitems_group.command()
@click.option('--data', type=str, help='JSON data for the menuitem')
@click.pass_context
def create(ctx, data):
    """Menu item creation is not part of this generated Spoonacular subset."""
    raise click.ClickException('Create is not implemented for the read-focused Spoonacular subset.')
