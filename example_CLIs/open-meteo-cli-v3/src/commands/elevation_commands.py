"""
CLI commands for elevation resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def elevation_group(ctx):
    """Manage Elevation resources."""
    ctx.obj = ctx.obj or {}


@elevation_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all elevation."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/v1/elevation')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@elevation_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a elevatio by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/v1/elevation/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@elevation_group.command()
@click.option('--data', type=str, help='JSON data for the elevatio')
@click.pass_context
def create(ctx, data):
    """Create a new elevatio."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/v1/elevation', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
