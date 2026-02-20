"""
CLI commands for REST Countries endpoints.
"""

import json

import click
import pandas as pd

from src.client import APIClient


def _emit_output(payload, output_format: str):
    if output_format == "json":
        click.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if isinstance(payload, dict):
        rows = [payload]
    else:
        rows = payload

    frame = pd.json_normalize(rows)
    if output_format == "csv":
        click.echo(frame.to_csv(index=False))
        return

    # For xlsx, save a default file path to avoid binary stdout output.
    output_file = "countries_output.xlsx"
    frame.to_excel(output_file, index=False)
    click.echo(f"Saved XLSX output to {output_file}")


def _request(ctx, endpoint: str, params=None, output_format: str = "json"):
    client = APIClient(ctx.obj["config"])
    result = client.get(endpoint, params=params)
    _emit_output(result, output_format)


@click.group()
@click.pass_context
def countries_group(ctx):
    """Manage Countries resources."""
    ctx.obj = ctx.obj or {}


@countries_group.command("all")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def all_countries(ctx, fields, output_format):
    """List all countries."""
    params = {"fields": fields} if fields else None
    _request(ctx, "/v3.1/all", params=params, output_format=output_format)


@countries_group.command()
@click.option("--status", type=click.Choice(["true", "false"]), default="true")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def independent(ctx, status, fields, output_format):
    """List countries by independence status."""
    params = {"status": status}
    if fields:
        params["fields"] = fields
    _request(ctx, "/v3.1/independent", params=params, output_format=output_format)


@countries_group.command("by-name")
@click.option("--name", required=True, help="Country name")
@click.option("--full-text", is_flag=True, help="Exact full-name match")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_name(ctx, name, full_text, fields, output_format):
    """Search countries by name."""
    params = {}
    if full_text:
        params["fullText"] = "true"
    if fields:
        params["fields"] = fields
    _request(ctx, f"/v3.1/name/{name}", params=params or None, output_format=output_format)


@countries_group.command("by-code")
@click.option("--code", required=True, help="Country code (cca2/cca3/ccn3/cioc)")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_code(ctx, code, fields, output_format):
    """Search a country by code."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/alpha/{code}", params=params, output_format=output_format)


@countries_group.command("by-codes")
@click.option("--codes", required=True, help="Comma-separated country codes")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_codes(ctx, codes, fields, output_format):
    """Search countries by multiple codes."""
    params = {"codes": codes}
    if fields:
        params["fields"] = fields
    _request(ctx, "/v3.1/alpha", params=params, output_format=output_format)


@countries_group.command("by-currency")
@click.option("--currency", required=True, help="Currency code or name")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_currency(ctx, currency, fields, output_format):
    """Search countries by currency."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/currency/{currency}", params=params, output_format=output_format)


@countries_group.command("by-demonym")
@click.option("--demonym", required=True, help="Demonym")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_demonym(ctx, demonym, fields, output_format):
    """Search countries by demonym."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/demonym/{demonym}", params=params, output_format=output_format)


@countries_group.command("by-language")
@click.option("--language", required=True, help="Language code or name")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_language(ctx, language, fields, output_format):
    """Search countries by language."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/lang/{language}", params=params, output_format=output_format)


@countries_group.command("by-capital")
@click.option("--capital", required=True, help="Capital city")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_capital(ctx, capital, fields, output_format):
    """Search countries by capital city."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/capital/{capital}", params=params, output_format=output_format)


@countries_group.command("by-region")
@click.option("--region", required=True, help="Region name")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_region(ctx, region, fields, output_format):
    """Search countries by region."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/region/{region}", params=params, output_format=output_format)


@countries_group.command("by-subregion")
@click.option("--subregion", required=True, help="Subregion name")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_subregion(ctx, subregion, fields, output_format):
    """Search countries by subregion."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/subregion/{subregion}", params=params, output_format=output_format)


@countries_group.command("by-translation")
@click.option("--translation", required=True, help="Translated country name")
@click.option("--fields", type=str, help="Comma-separated response fields")
@click.option("--format", "output_format", type=click.Choice(["json", "csv", "xlsx"]), default="json")
@click.pass_context
def by_translation(ctx, translation, fields, output_format):
    """Search countries by translation."""
    params = {"fields": fields} if fields else None
    _request(ctx, f"/v3.1/translation/{translation}", params=params, output_format=output_format)
