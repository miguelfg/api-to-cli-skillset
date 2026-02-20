"""
CLI commands for user resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def user_group(ctx):
    """Manage User resources."""
    ctx.obj = ctx.obj or {}


@user_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all user."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/user')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@user_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a use by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/user/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@user_group.command()
@click.option('--data', type=str, help='JSON data for the use')
@click.pass_context
def create(ctx, data):
    """Create a new use."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/user', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
