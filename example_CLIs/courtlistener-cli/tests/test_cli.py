"""Basic tests for CourtListener CLI"""

import pytest
from click.testing import CliRunner
from src.cli import main


def test_cli_help():
    """Test CLI help command"""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'CourtListener' in result.output


def test_cli_version():
    """Test CLI version"""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert '1.0.0' in result.output


def test_opinions_help():
    """Test opinions command help"""
    runner = CliRunner()
    result = runner.invoke(main, ['opinions', '--help'])
    assert result.exit_code == 0
    assert 'opinions' in result.output.lower()
