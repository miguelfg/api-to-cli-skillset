"""Basic CLI smoke tests using Click's test runner."""

from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def mock_client():
    with patch("src.cli.TronscanClient") as MockCls:
        instance = MagicMock()
        MockCls.return_value = instance
        yield instance


def invoke(runner: CliRunner, args: list, env: dict | None = None) -> object:
    return runner.invoke(cli, args, obj={}, env=env or {"TRONSCAN_API_KEY": "test-key"}, catch_exceptions=False)


# ── accounts ──────────────────────────────────────────────────────────────────

def test_accounts_list_dry_run(runner, mock_client):
    result = invoke(runner, ["accounts", "list", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


def test_accounts_get_dry_run(runner, mock_client):
    result = invoke(runner, ["accounts", "get", "--address", "TAddr123", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


def test_accounts_tokens_dry_run(runner, mock_client):
    result = invoke(runner, ["accounts", "tokens", "--address", "TAddr123", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


# ── blocks ────────────────────────────────────────────────────────────────────

def test_blocks_list_dry_run(runner, mock_client):
    result = invoke(runner, ["blocks", "list", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


def test_blocks_stats_dry_run(runner, mock_client):
    result = invoke(runner, ["blocks", "stats", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


# ── contracts ─────────────────────────────────────────────────────────────────

def test_contracts_list_dry_run(runner, mock_client):
    result = invoke(runner, ["contracts", "list", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


def test_contracts_get_dry_run(runner, mock_client):
    result = invoke(runner, ["contracts", "get", "--contract", "TAddr_contract", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


def test_contracts_events_dry_run(runner, mock_client):
    result = invoke(runner, ["contracts", "events", "--contract-address", "TAddr_contract", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.output


# ── missing api key ───────────────────────────────────────────────────────────

def test_missing_api_key(runner):
    result = runner.invoke(cli, ["accounts", "list"], obj={}, env={"TRONSCAN_API_KEY": ""})
    assert result.exit_code == 1
