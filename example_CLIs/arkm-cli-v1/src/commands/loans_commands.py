"""
CLI commands for loans resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def loans_group(ctx):
    """Manage Loans resources."""
    ctx.obj = ctx.obj or {}


@loans_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all loans."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/loans/entity/{entity}')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@loans_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a loan by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/loans/entity/{entity}/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@loans_group.command()
@click.option('--data', type=str, help='JSON data for the loan')
@click.pass_context
def create(ctx, data):
    """Create a new loan."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/loans/entity/{entity}', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
