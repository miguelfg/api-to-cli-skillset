"""
CLI commands for tag resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def tag_group(ctx):
    """Manage Tag resources."""
    ctx.obj = ctx.obj or {}


@tag_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all tag."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/tag')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@tag_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a ta by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/tag/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@tag_group.command()
@click.option('--data', type=str, help='JSON data for the ta')
@click.pass_context
def create(ctx, data):
    """Create a new ta."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/tag', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
