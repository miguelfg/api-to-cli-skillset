# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Repository Guidelines

## Project Structure & Module Organization
This repository is a skillset for turning API docs into Python CLI projects. Core assets live in `skills/`:
- `skills/api-to-doc/`: URL/docs to OpenAPI (`scripts/`, `references/`, `assets/`)
- `skills/doc-to-prd/`: OpenAPI/docs to PRD templates and guidance
- `skills/prd-to-cli/`: PRD to generated Click CLI projects

Examples and reference outputs are in `example_APIs/`, `example_PRDs/`, and `example_CLIs/tronscan-cli/`. Supporting documentation is in `docs/`.

## Current Workflow

The repository now supports a three-step workflow:

1. `api-to-doc`: convert API documentation URLs or API docs into an OpenAPI 3.0.0 YAML spec
2. `doc-to-prd`: convert an OpenAPI spec or API docs into an implementation-ready PRD
3. `prd-to-cli`: generate a Python Click CLI project from that PRD

Use the skill-specific `SKILL.md` files as the source of truth for execution details:
- `skills/api-to-doc/SKILL.md`
- `skills/doc-to-prd/SKILL.md`
- `skills/prd-to-cli/SKILL.md`

Do not rely on older two-step repo descriptions or Claude-specific tool assumptions. The skill instructions in `skills/*/SKILL.md` define the current behavior.

## Build, Test, and Development Commands
There is no single root build pipeline; work is script-driven.
- `python skills/api-to-doc/scripts/fetch_api_info.py <url> --no-cache`: fetch and parse API docs
- `python skills/api-to-doc/scripts/crawler.py <start_url>`: crawl multi-page API docs
- `python skills/prd-to-cli/scripts/generate_cli_from_prd.py <prd_file> <output_dir> [project_name]`: generate a CLI project from a PRD
- `python -m src.cli --help` (inside a generated CLI project): verify CLI wiring
- `pytest tests/ -v` (inside generated projects when tests exist): run tests

## Coding Style & Naming Conventions
Use Python 3 with 4-space indentation and snake_case for files, functions, and variables. Keep modules focused and small (`scripts/` for executable workflows, `references/` for specs). Prefer descriptive script names like `generate_*`, `fetch_*`, `*_extractor.py`. For Markdown specs/templates, use clear heading hierarchies and concise sections.

When updating skills:
- edit files directly under `skills/{skill-name}/`
- keep `SKILL.md` aligned with the actual scripts and templates
- prefer reusing `scripts/`, `references/`, `templates/`, and `assets/` rather than recreating content manually

## Testing Guidelines
For this repository, validate by running the skill scripts on sample inputs in `example_APIs/` and checking generated artifacts. For generated CLI projects, use `pytest` where available and smoke-test key commands such as `python -m src.cli <resource> <command>`. Favor deterministic outputs so repeated runs are comparable.

Good validation targets include:
- `example_APIs/petstore.json`
- `example_APIs/github-api.json`
- `example_APIs/stripe-api.json`
- files in `example_PRDs/`
- generated projects in `example_CLIs/`

## Commit & Pull Request Guidelines
Follow the existing commit style: short, imperative subjects such as `Add ...`, `Enhance ...`, `Update ...`, or `Clean up ...`. Keep commits scoped to one logical change. PRs should include:
- what changed and why
- paths affected (for example, `skills/prd-to-cli/scripts/...`)
- validation performed (commands run, sample inputs/outputs)
- any follow-up work or known limitations

## Security & Configuration Tips
Never commit secrets. Keep API keys in `.env` files and ensure they stay git-ignored. Share sanitized example configs only, such as `.env.example`.

## Practical Notes

- Treat `README.md` and the per-skill `SKILL.md` files as the authoritative product and workflow references.
- If the skill behavior and a prose doc disagree, update the prose doc to match the implementation or fix the implementation and then sync the doc.
- Keep documentation grounded in the current repository state. Do not document unsupported features as if they are complete.
