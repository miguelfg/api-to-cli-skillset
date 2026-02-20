.PHONY: help install install-dev lint format test run

PROJECT_NAME := open-meteo-cli-v3

help:
	@echo "open-meteo-cli-v3 - Available commands"
	@echo ""
	@echo "  make install      Install dependencies with uv"
	@echo "  make install-dev  Install dependencies including dev extras"
	@echo "  make lint         Run basic lint checks"
	@echo "  make format       Format source code"
	@echo "  make test         Run tests"
	@echo "  make run          Show CLI help"
	@echo ""
	@echo "  CLI examples:"
	@echo "  make overview-list Example: uv run $(PROJECT_NAME) overview list"
	@echo "  make purpose-list Example: uv run $(PROJECT_NAME) purpose list"
	@echo "  make requirements-list Example: uv run $(PROJECT_NAME) requirements list"
	@echo "  make setup-list   Example: uv run $(PROJECT_NAME) setup list"
	@echo "  make verify-list  Example: uv run $(PROJECT_NAME) verify list"
	@echo "  make method-list  Example: uv run $(PROJECT_NAME) method list"
	@echo "  make strategy-list Example: uv run $(PROJECT_NAME) strategy list"

install:
	uv sync

install-dev:
	uv sync --all-extras

lint:
	uv run python -m py_compile src/*.py src/commands/*.py

format:
	uv run black src/
	uv run isort src/

test:
	uv run pytest tests/ -v

run:
	uv run $(PROJECT_NAME) --help

batch-example:
	uv run $(PROJECT_NAME) batch --input-file data/batch.csv --format json --output-path ./output

overview-list:
	uv run $(PROJECT_NAME) overview list

purpose-list:
	uv run $(PROJECT_NAME) purpose list

requirements-list:
	uv run $(PROJECT_NAME) requirements list

setup-list:
	uv run $(PROJECT_NAME) setup list

verify-list:
	uv run $(PROJECT_NAME) verify list

method-list:
	uv run $(PROJECT_NAME) method list

strategy-list:
	uv run $(PROJECT_NAME) strategy list

.DEFAULT_GOAL := help
