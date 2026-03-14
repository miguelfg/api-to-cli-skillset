.PHONY: help install install-dev lint format test run

PROJECT_NAME := spoonacular-cli

help:
	@echo "spoonacular-cli - Available commands"
	@echo ""
	@echo "  make install      Install dependencies with uv"
	@echo "  make install-dev  Install dependencies including dev extras"
	@echo "  make lint         Run basic lint checks"
	@echo "  make format       Format source code"
	@echo "  make test         Run tests"
	@echo "  make run          Show CLI help"
	@echo ""
	@echo "  CLI examples:"
	@echo "  make recipes-list Example: uv run $(PROJECT_NAME) recipes list"
	@echo "  make ingredients-list Example: uv run $(PROJECT_NAME) ingredients list"
	@echo "  make products-list Example: uv run $(PROJECT_NAME) products list"
	@echo "  make menuitems-list Example: uv run $(PROJECT_NAME) menuitems list"
	@echo "  make mealplanner-list Example: uv run $(PROJECT_NAME) mealplanner list"

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

recipes-list:
	uv run $(PROJECT_NAME) recipes list

ingredients-list:
	uv run $(PROJECT_NAME) ingredients list

products-list:
	uv run $(PROJECT_NAME) products list

menuitems-list:
	uv run $(PROJECT_NAME) menuitems list

mealplanner-list:
	uv run $(PROJECT_NAME) mealplanner list

.DEFAULT_GOAL := help
