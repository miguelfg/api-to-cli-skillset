"""
CLI commands for gfs resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def gfs_group(ctx):
    """Manage Gfs resources."""
    ctx.obj = ctx.obj or {}


@gfs_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all gfs."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/v1/gfs')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@gfs_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a gf by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/v1/gfs/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@gfs_group.command()
@click.option('--data', type=str, help='JSON data for the gf')
@click.pass_context
def create(ctx, data):
    """Create a new gf."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/v1/gfs', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
