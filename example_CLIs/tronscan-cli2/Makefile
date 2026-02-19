.PHONY: help install install-dev lint format test test-cov clean build \
        accounts-list accounts-get accounts-tokens \
        blocks-list blocks-stats \
        contracts-list contracts-get contracts-events

PROJECT_NAME := tronscan

help:
	@echo "tronscan-cli — Available commands:"
	@echo ""
	@echo "  Setup:"
	@echo "    make install           Install dependencies (uv sync)"
	@echo "    make install-dev       Install with dev dependencies"
	@echo ""
	@echo "  Development:"
	@echo "    make lint              Run linters (black + pylint)"
	@echo "    make format            Format code (black + isort)"
	@echo "    make test              Run tests"
	@echo "    make test-cov          Run tests with coverage"
	@echo "    make clean             Clean build artifacts"
	@echo ""
	@echo "  Accounts:"
	@echo "    make accounts-list     List top accounts by balance"
	@echo "    make accounts-get      Get account details (ADDRESS=...)"
	@echo "    make accounts-tokens   List account tokens (ADDRESS=...)"
	@echo ""
	@echo "  Blocks:"
	@echo "    make blocks-list       List latest blocks"
	@echo "    make blocks-stats      Get block statistics"
	@echo ""
	@echo "  Contracts:"
	@echo "    make contracts-list    List smart contracts"
	@echo "    make contracts-get     Get contract details (CONTRACT=...)"
	@echo "    make contracts-events  Get contract events (CONTRACT=...)"
	@echo ""
	@echo "  Batch:"
	@echo "    make batch             Run batch from data/batch.txt"

install:
	uv sync

install-dev:
	uv sync --all-extras

lint:
	uv run black --check src/
	uv run pylint src/

format:
	uv run black src/
	uv run isort src/

test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ -v --cov=src/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	uv build

# ── Accounts ──────────────────────────────────────────────────────────────────

accounts-list:
	uv run python -m src.cli accounts list --limit 20 --sort -balance

accounts-get:
	@test -n "$(ADDRESS)" || (echo "Usage: make accounts-get ADDRESS=TAddr..." && exit 1)
	uv run python -m src.cli accounts get --address $(ADDRESS)

accounts-tokens:
	@test -n "$(ADDRESS)" || (echo "Usage: make accounts-tokens ADDRESS=TAddr..." && exit 1)
	uv run python -m src.cli accounts tokens --address $(ADDRESS) --limit 20

# ── Blocks ────────────────────────────────────────────────────────────────────

blocks-list:
	uv run python -m src.cli blocks list --limit 20

blocks-stats:
	uv run python -m src.cli blocks stats

# ── Contracts ─────────────────────────────────────────────────────────────────

contracts-list:
	uv run python -m src.cli contracts list --limit 20

contracts-get:
	@test -n "$(CONTRACT)" || (echo "Usage: make contracts-get CONTRACT=TAddr..." && exit 1)
	uv run python -m src.cli contracts get --contract $(CONTRACT)

contracts-events:
	@test -n "$(CONTRACT)" || (echo "Usage: make contracts-events CONTRACT=TAddr..." && exit 1)
	uv run python -m src.cli contracts events --contract-address $(CONTRACT) --limit 50

# ── Batch ─────────────────────────────────────────────────────────────────────

batch:
	uv run python -m src.cli batch --input-file data/batch.txt --output-dir output/

.DEFAULT_GOAL := help
