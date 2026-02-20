"""
CLI commands for strategy resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def strategy_group(ctx):
    """Manage Strategy resources."""
    ctx.obj = ctx.obj or {}


@strategy_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all strategy."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/strategy')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@strategy_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a strateg by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/strategy/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@strategy_group.command()
@click.option('--data', type=str, help='JSON data for the strateg')
@click.pass_context
def create(ctx, data):
    """Create a new strateg."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/strategy', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
