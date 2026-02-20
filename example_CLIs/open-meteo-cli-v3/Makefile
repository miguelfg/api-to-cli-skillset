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
	@echo "  make airquality-list Example: uv run $(PROJECT_NAME) airquality list"
	@echo "  make archive-list Example: uv run $(PROJECT_NAME) archive list"
	@echo "  make bom-list     Example: uv run $(PROJECT_NAME) bom list"
	@echo "  make climate-list Example: uv run $(PROJECT_NAME) climate list"
	@echo "  make cma-list     Example: uv run $(PROJECT_NAME) cma list"
	@echo "  make dmi-list     Example: uv run $(PROJECT_NAME) dmi list"
	@echo "  make dwdicon-list Example: uv run $(PROJECT_NAME) dwdicon list"
	@echo "  make ecmwf-list   Example: uv run $(PROJECT_NAME) ecmwf list"

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

airquality-list:
	uv run $(PROJECT_NAME) airquality list

archive-list:
	uv run $(PROJECT_NAME) archive list

bom-list:
	uv run $(PROJECT_NAME) bom list

climate-list:
	uv run $(PROJECT_NAME) climate list

cma-list:
	uv run $(PROJECT_NAME) cma list

dmi-list:
	uv run $(PROJECT_NAME) dmi list

dwdicon-list:
	uv run $(PROJECT_NAME) dwdicon list

ecmwf-list:
	uv run $(PROJECT_NAME) ecmwf list

.DEFAULT_GOAL := help
