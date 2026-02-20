"""
CLI commands for balances resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def balances_group(ctx):
    """Manage Balances resources."""
    ctx.obj = ctx.obj or {}


@balances_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all balances."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/balances/entity/{entity}')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@balances_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a balance by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/balances/entity/{entity}/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@balances_group.command()
@click.option('--data', type=str, help='JSON data for the balance')
@click.pass_context
def create(ctx, data):
    """Create a new balance."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/balances/entity/{entity}', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
