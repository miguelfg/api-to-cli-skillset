"""
CLI commands for airquality resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def airquality_group(ctx):
    """Manage Airquality resources."""
    ctx.obj = ctx.obj or {}


@airquality_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all airquality."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/v1/air-quality')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@airquality_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a airqualit by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/v1/air-quality/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@airquality_group.command()
@click.option('--data', type=str, help='JSON data for the airqualit')
@click.pass_context
def create(ctx, data):
    """Create a new airqualit."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/v1/air-quality', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
