"""
Basic CLI smoke tests for generated projects.
"""

from click.testing import CliRunner

from src.cli import cli


def test_root_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "batch" in result.output


def test_batch_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["batch", "--help"])
    assert result.exit_code == 0
