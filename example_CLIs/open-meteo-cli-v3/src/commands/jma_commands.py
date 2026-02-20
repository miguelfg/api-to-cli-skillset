"""
CLI commands for jma resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def jma_group(ctx):
    """Manage Jma resources."""
    ctx.obj = ctx.obj or {}


@jma_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all jma."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/v1/jma')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@jma_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a jm by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/v1/jma/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@jma_group.command()
@click.option('--data', type=str, help='JSON data for the jm')
@click.pass_context
def create(ctx, data):
    """Create a new jm."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/v1/jma', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
