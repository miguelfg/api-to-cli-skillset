"""
CLI commands for volume resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def volume_group(ctx):
    """Manage Volume resources."""
    ctx.obj = ctx.obj or {}


@volume_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all volume."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/volume')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@volume_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a volum by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/volume/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@volume_group.command()
@click.option('--data', type=str, help='JSON data for the volum')
@click.pass_context
def create(ctx, data):
    """Create a new volum."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/volume', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
