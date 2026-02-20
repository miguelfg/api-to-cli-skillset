"""
CLI commands for arkm resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def arkm_group(ctx):
    """Manage Arkm resources."""
    ctx.obj = ctx.obj or {}


@arkm_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all arkm."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/arkm')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@arkm_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a ark by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/arkm/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@arkm_group.command()
@click.option('--data', type=str, help='JSON data for the ark')
@click.pass_context
def create(ctx, data):
    """Create a new ark."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/arkm', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
