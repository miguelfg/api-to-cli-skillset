.PHONY: help install install-dev ensure-dev-deps format lint lint-fix check test validate clean \
	check-clean-git tag tag-patch tag-minor tag-major tag-push

SRC_DIRS := skills
PY_FILES := $(shell find $(SRC_DIRS) -type f -name '*.py' \
	-not -path '*/.venv/*' \
	-not -path '*/__pycache__/*')
TAG_PREFIX ?= v

help:
	@echo "Repository quality targets"
	@echo ""
	@echo "  make install       Install repository dependencies"
	@echo "  make install-dev   Install repository dependencies + dev extras"
	@echo "  make format        Format Python code (ruff format, fallback: black + isort)"
	@echo "  make lint          Lint Python code (ruff check, fallback: py_compile)"
	@echo "  make lint-fix      Auto-fix lint issues (ruff --fix, fallback: black + isort)"
	@echo "  make check         Run format + lint + syntax checks"
	@echo "  make test          Run root-level tests when present"
	@echo "  make validate      check + test"
	@echo "  make tag VERSION=vX.Y.Z  Create an annotated git tag"
	@echo "  make tag-patch     Create next patch tag from latest"
	@echo "  make tag-minor     Create next minor tag from latest"
	@echo "  make tag-major     Create next major tag from latest"
	@echo "  make tag-push      Push all tags to origin"
	@echo "  make clean         Remove Python caches"

install:
	uv sync

install-dev:
	uv sync --all-extras

ensure-dev-deps:
	@uv sync --all-extras

format: ensure-dev-deps
	@if uv run ruff --version >/dev/null 2>&1; then \
		uv run ruff format $(SRC_DIRS); \
	elif uv run black --version >/dev/null 2>&1; then \
		uv run black $(SRC_DIRS); \
		if uv run isort --version >/dev/null 2>&1; then uv run isort $(SRC_DIRS); fi; \
	else \
		echo "No formatter installed (ruff/black)."; \
		exit 1; \
	fi

lint: ensure-dev-deps
	@if uv run ruff --version >/dev/null 2>&1; then \
		uv run ruff check $(SRC_DIRS); \
	else \
		uv run python -m py_compile $(PY_FILES); \
	fi

lint-fix: ensure-dev-deps
	@if uv run ruff --version >/dev/null 2>&1; then \
		uv run ruff check $(SRC_DIRS) --fix; \
		uv run ruff format $(SRC_DIRS); \
	elif uv run black --version >/dev/null 2>&1; then \
		uv run black $(SRC_DIRS); \
		if uv run isort --version >/dev/null 2>&1; then uv run isort $(SRC_DIRS); fi; \
	else \
		echo "No lint/format tools installed (ruff/black)."; \
		exit 1; \
	fi

check: format lint
	@uv run python -m py_compile $(PY_FILES)

test: ensure-dev-deps
	@if [ -d tests ]; then \
		if uv run pytest --version >/dev/null 2>&1; then \
			uv run pytest tests -v; \
		else \
			echo "pytest not installed"; exit 1; \
		fi; \
	else \
		echo "No root tests directory found; skipping."; \
	fi

validate: check test

clean:
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete

check-clean-git:
	@if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then \
		echo "Not a git repository."; exit 1; \
	fi
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Working tree is not clean. Commit/stash changes before tagging."; \
		exit 1; \
	fi

tag: check-clean-git
	@if [ -z "$(VERSION)" ]; then \
		echo "Usage: make tag VERSION=$(TAG_PREFIX)X.Y.Z"; \
		exit 1; \
	fi
	@if ! echo "$(VERSION)" | grep -Eq "^$(TAG_PREFIX)[0-9]+\.[0-9]+\.[0-9]+$$"; then \
		echo "Invalid VERSION format: $(VERSION). Expected $(TAG_PREFIX)X.Y.Z"; \
		exit 1; \
	fi
	@if git rev-parse "$(VERSION)" >/dev/null 2>&1; then \
		echo "Tag already exists: $(VERSION)"; \
		exit 1; \
	fi
	@git tag -a "$(VERSION)" -m "Release $(VERSION)"
	@echo "Created tag $(VERSION)"

tag-patch: check-clean-git
	@latest=$$(git tag --list "$(TAG_PREFIX)[0-9]*.[0-9]*.[0-9]*" | sort -V | tail -1); \
	if [ -z "$$latest" ]; then \
		next="$(TAG_PREFIX)0.0.1"; \
	else \
		base=$${latest#$(TAG_PREFIX)}; \
		maj=$$(echo "$$base" | cut -d. -f1); \
		min=$$(echo "$$base" | cut -d. -f2); \
		pat=$$(echo "$$base" | cut -d. -f3); \
		next="$(TAG_PREFIX)$$maj.$$min.$$((pat+1))"; \
	fi; \
	$(MAKE) tag VERSION=$$next

tag-minor: check-clean-git
	@latest=$$(git tag --list "$(TAG_PREFIX)[0-9]*.[0-9]*.[0-9]*" | sort -V | tail -1); \
	if [ -z "$$latest" ]; then \
		next="$(TAG_PREFIX)0.1.0"; \
	else \
		base=$${latest#$(TAG_PREFIX)}; \
		maj=$$(echo "$$base" | cut -d. -f1); \
		min=$$(echo "$$base" | cut -d. -f2); \
		next="$(TAG_PREFIX)$$maj.$$((min+1)).0"; \
	fi; \
	$(MAKE) tag VERSION=$$next

tag-major: check-clean-git
	@latest=$$(git tag --list "$(TAG_PREFIX)[0-9]*.[0-9]*.[0-9]*" | sort -V | tail -1); \
	if [ -z "$$latest" ]; then \
		next="$(TAG_PREFIX)1.0.0"; \
	else \
		base=$${latest#$(TAG_PREFIX)}; \
		maj=$$(echo "$$base" | cut -d. -f1); \
		next="$(TAG_PREFIX)$$((maj+1)).0.0"; \
	fi; \
	$(MAKE) tag VERSION=$$next

tag-push:
	@git push --tags
	@echo "Pushed tags to origin"
