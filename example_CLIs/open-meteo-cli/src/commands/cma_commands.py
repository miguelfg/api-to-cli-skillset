"""
CLI commands for cma resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def cma_group(ctx):
    """Manage Cma resources."""
    ctx.obj = ctx.obj or {}


@cma_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all cma."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/cma')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cma_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a cm by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/cma/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cma_group.command()
@click.option('--data', type=str, help='JSON data for the cm')
@click.pass_context
def create(ctx, data):
    """Create a new cm."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/cma', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
