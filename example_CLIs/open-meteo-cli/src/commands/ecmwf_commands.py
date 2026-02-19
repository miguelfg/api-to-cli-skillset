"""
CLI commands for ecmwf resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def ecmwf_group(ctx):
    """Manage Ecmwf resources."""
    ctx.obj = ctx.obj or {}


@ecmwf_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all ecmwf."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/ecmwf')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@ecmwf_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a ecmw by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/ecmwf/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@ecmwf_group.command()
@click.option('--data', type=str, help='JSON data for the ecmw')
@click.pass_context
def create(ctx, data):
    """Create a new ecmw."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/ecmwf', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
