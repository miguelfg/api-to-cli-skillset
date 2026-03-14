"""
CLI commands for mealplanner resource.
"""

import click
from src.client import APIClient


@click.group()
@click.pass_context
def mealplanner_group(ctx):
    """Manage Mealplanner resources."""
    ctx.obj = ctx.obj or {}


@mealplanner_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
@click.option(
    '--time-frame',
    type=click.Choice(['day', 'week']),
    default='day',
    show_default=True,
    help='Meal plan period',
)
@click.option('--target-calories', type=int, help='Daily calorie target')
@click.option('--diet', type=str, help='Diet filter')
@click.option('--exclude', type=str, help='Comma-separated exclusions')
@click.pass_context
def list(ctx, format, time_frame, target_calories, diet, exclude):
    """List all mealplanner."""
    client = APIClient(ctx.obj['config'])
    try:
        results = client.get(
            '/mealplanner/generate',
            params={
                'timeFrame': time_frame,
                'targetCalories': target_calories,
                'diet': diet,
                'exclude': exclude,
            },
        )
        if format == 'json':
            import json
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Format {format} not yet implemented")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@mealplanner_group.command()
@click.argument('id')
@click.option('--target-calories', type=int, help='Daily calorie target')
@click.option('--diet', type=str, help='Diet filter')
@click.option('--exclude', type=str, help='Comma-separated exclusions')
@click.pass_context
def get(ctx, id, target_calories, diet, exclude):
    """Get a day or week meal plan."""
    client = APIClient(ctx.obj['config'])
    try:
        result = client.get(
            '/mealplanner/generate',
            params={
                'timeFrame': id,
                'targetCalories': target_calories,
                'diet': diet,
                'exclude': exclude,
            },
        )
        import json
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@mealplanner_group.command()
@click.option('--data', type=str, help='JSON data for the mealplanne')
@click.pass_context
def create(ctx, data):
    """Meal planner creation is not part of this generated Spoonacular subset."""
    raise click.ClickException('Create is not implemented for the read-focused Spoonacular subset.')
