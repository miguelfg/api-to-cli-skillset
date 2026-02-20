from click.testing import CliRunner

from src.cli import cli


def _run_with_stubbed_get(monkeypatch, args):
    captured = {}

    def fake_get(self, endpoint, params=None):
        captured["endpoint"] = endpoint
        captured["params"] = params
        return [{"name": {"common": "Germany"}}]

    monkeypatch.setattr("src.client.APIClient.get", fake_get)
    runner = CliRunner()
    result = runner.invoke(cli, args)
    return result, captured


def test_root_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "countries" in result.output
    assert "batch" in result.output


def test_countries_help_lists_restcountries_commands():
    runner = CliRunner()
    result = runner.invoke(cli, ["countries", "--help"])
    assert result.exit_code == 0
    assert "all" in result.output
    assert "independent" in result.output
    assert "by-name" in result.output
    assert "by-code" in result.output
    assert "by-currency" in result.output


def test_by_name_maps_to_expected_endpoint_and_query(monkeypatch):
    result, captured = _run_with_stubbed_get(
        monkeypatch,
        ["countries", "by-name", "--name", "germany", "--full-text", "--fields", "name,capital"],
    )
    assert result.exit_code == 0
    assert captured["endpoint"] == "/v3.1/name/germany"
    assert captured["params"] == {"fullText": "true", "fields": "name,capital"}


def test_by_codes_maps_to_alpha_endpoint(monkeypatch):
    result, captured = _run_with_stubbed_get(
        monkeypatch,
        ["countries", "by-codes", "--codes", "deu,fra", "--fields", "name"],
    )
    assert result.exit_code == 0
    assert captured["endpoint"] == "/v3.1/alpha"
    assert captured["params"] == {"codes": "deu,fra", "fields": "name"}


def test_independent_defaults_status_true(monkeypatch):
    result, captured = _run_with_stubbed_get(monkeypatch, ["countries", "independent"])
    assert result.exit_code == 0
    assert captured["endpoint"] == "/v3.1/independent"
    assert captured["params"] == {"status": "true"}
