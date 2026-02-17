# Repository Guidelines

## Project Structure & Module Organization
This repository is a skillset for turning API docs into Python CLI projects. Core assets live in `skills/`:
- `skills/api-to-doc/`: URL/docs to OpenAPI (`scripts/`, `references/`, `assets/`)
- `skills/doc-to-prd/`: OpenAPI/docs to PRD templates and guidance
- `skills/prd-to-cli/`: PRD to generated Click CLI projects

Examples and reference outputs are in `example_APIs/`, `example_PRDs/`, and `example_CLIs/tronscan-cli/`. Supporting documentation is in `docs/`.

## Build, Test, and Development Commands
There is no single root build pipeline; work is script-driven.
- `python skills/api-to-doc/scripts/fetch_api_info.py <url> --no-cache`: fetch and parse API docs.
- `python skills/api-to-doc/scripts/crawler.py <start_url>`: crawl multi-page API docs.
- `python skills/prd-to-cli/scripts/generate_cli_from_prd.py <prd_file> <output_dir> [project_name]`: generate a CLI project from a PRD.
- `python -m src.cli --help` (inside a generated CLI project): verify CLI wiring.
- `pytest tests/ -v` (inside generated projects when tests exist): run tests.

## Coding Style & Naming Conventions
Use Python 3 with 4-space indentation and snake_case for files, functions, and variables. Keep modules focused and small (`scripts/` for executable workflows, `references/` for specs). Prefer descriptive script names like `generate_*`, `fetch_*`, `*_extractor.py`. For Markdown specs/templates, use clear heading hierarchies and concise sections.

## Testing Guidelines
For this repository, validate by running the skill scripts on sample inputs in `example_APIs/` and checking generated artifacts. For generated CLI projects, use `pytest` where available and smoke-test key commands (`python -m src.cli <resource> <command>`). Favor deterministic outputs so repeated runs are comparable.

## Commit & Pull Request Guidelines
Follow the existing commit style: short, imperative subjects (for example, `Add ...`, `Enhance ...`, `Update ...`, `Clean up ...`). Keep commits scoped to one logical change. PRs should include:
- What changed and why
- Paths affected (for example, `skills/prd-to-cli/scripts/...`)
- Validation performed (commands run, sample inputs/outputs)
- Any follow-up work or known limitations

## Security & Configuration Tips
Never commit secrets. Keep API keys in `.env` files and ensure they stay git-ignored. Share sanitized example configs only (for example, `.env.example`).
