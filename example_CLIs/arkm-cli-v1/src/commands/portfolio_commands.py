"""
CLI commands for portfolio resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def portfolio_group(ctx):
    """Manage Portfolio resources."""
    ctx.obj = ctx.obj or {}


@portfolio_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all portfolio."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/portfolio')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@portfolio_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a portfoli by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/portfolio/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@portfolio_group.command()
@click.option('--data', type=str, help='JSON data for the portfoli')
@click.pass_context
def create(ctx, data):
    """Create a new portfoli."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/portfolio', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
