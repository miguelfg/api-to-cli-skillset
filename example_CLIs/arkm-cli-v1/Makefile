.PHONY: help install install-dev lint format test run

PROJECT_NAME := arkm-cli-v1

help:
	@echo "arkm-cli-v1 - Available commands"
	@echo ""
	@echo "  make install      Install dependencies with uv"
	@echo "  make install-dev  Install dependencies including dev extras"
	@echo "  make lint         Run basic lint checks"
	@echo "  make format       Format source code"
	@echo "  make test         Run tests"
	@echo "  make run          Show CLI help"
	@echo ""
	@echo "  CLI examples:"
	@echo "  make arkm-list    Example: uv run $(PROJECT_NAME) arkm list"
	@echo "  make balances-list Example: uv run $(PROJECT_NAME) balances list"
	@echo "  make chains-list  Example: uv run $(PROJECT_NAME) chains list"
	@echo "  make cluster-list Example: uv run $(PROJECT_NAME) cluster list"
	@echo "  make counterparties-list Example: uv run $(PROJECT_NAME) counterparties list"
	@echo "  make flow-list    Example: uv run $(PROJECT_NAME) flow list"
	@echo "  make history-list Example: uv run $(PROJECT_NAME) history list"
	@echo "  make intelligence-list Example: uv run $(PROJECT_NAME) intelligence list"

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

arkm-list:
	uv run $(PROJECT_NAME) arkm list

balances-list:
	uv run $(PROJECT_NAME) balances list

chains-list:
	uv run $(PROJECT_NAME) chains list

cluster-list:
	uv run $(PROJECT_NAME) cluster list

counterparties-list:
	uv run $(PROJECT_NAME) counterparties list

flow-list:
	uv run $(PROJECT_NAME) flow list

history-list:
	uv run $(PROJECT_NAME) history list

intelligence-list:
	uv run $(PROJECT_NAME) intelligence list

.DEFAULT_GOAL := help
