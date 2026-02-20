"""
CLI commands for marketdata resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def marketdata_group(ctx):
    """Manage Marketdata resources."""
    ctx.obj = ctx.obj or {}


@marketdata_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.pass_context
def list(ctx, format):
    """List all marketdata."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get('/marketdata/altcoin_index')
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@marketdata_group.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Get a marketdat by ID."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get('/marketdata/altcoin_index/{id}')
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@marketdata_group.command()
@click.option('--data', type=str, help='JSON data for the marketdat')
@click.pass_context
def create(ctx, data):
    """Create a new marketdat."""
    client = APIClient(ctx.obj['config'])
    try:
        import json
        payload = json.loads(data) if data else {}
        result = client.post('/marketdata/altcoin_index', payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
