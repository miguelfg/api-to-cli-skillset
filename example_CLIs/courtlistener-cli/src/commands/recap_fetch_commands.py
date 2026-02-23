"""Click commands for recap-fetch resource"""

import click
import json
from ..client import CourtListenerClient
from ..output import save_json, save_csv, save_xlsx
from pathlib import Path


@click.group()
def recap_fetch():
    """RecapFetch management"""
    pass


@recap_fetch.command('list')
@click.option('--limit', default=20, help='Results per page')
@click.option('--offset', default=0, help='Pagination offset')
@click.option('--format', 'output_format', default='json',
              type=click.Choice(['json', 'csv', 'xlsx']))
@click.option('--output', 'output_path', default='./output',
              type=click.Path())
def list_recap_fetch(limit, offset, output_format, output_path):
    """List recap-fetch"""
    client = CourtListenerClient()
    
    params = {'limit': limit, 'offset': offset}
    
    try:
        result = client.get('/recap-fetch/', params=params)
        
        output_dir = Path(output_path)
        output_dir.mkdir(exist_ok=True)
        
        if 'results' in result:
            if output_format == 'json':
                filepath = save_json(result, output_dir)
            elif output_format == 'csv':
                filepath = save_csv(result['results'], output_dir)
            else:  # xlsx
                filepath = save_xlsx(result['results'], output_dir)
            
            click.echo(f"✓ Retrieved {len(result['results'])} items")
            click.echo(f"✓ Saved to {filepath}")
        else:
            click.echo("No data found")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@recap_fetch.command('get')
@click.argument('recap_fetch_id', type=int)
def get_recap_fetch(recap_fetch_id):
    """Get recap-fetch by ID"""
    client = CourtListenerClient()
    
    try:
        result = client.get('/recap-fetch/({id})/')
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
