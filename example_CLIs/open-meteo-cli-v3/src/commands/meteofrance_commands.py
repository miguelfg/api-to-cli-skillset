"""
CLI commands for meteofrance resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def meteofrance_group(ctx):
    """Manage Meteofrance resources."""
    ctx.obj = ctx.obj or {}


@meteofrance_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all meteofrance."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/v1/meteofrance')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@meteofrance_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a meteofranc by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/v1/meteofrance/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@meteofrance_group.command()
@click.option('--data', type=str, help='JSON data for the meteofranc')
@click.pass_context
def create(ctx, data):
    """Create a new meteofranc."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/v1/meteofrance', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
