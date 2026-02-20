# API-to-CLI Skillset

Convert API docs/specs into Python CLI projects in three steps:

1. `api-to-doc` -> OpenAPI (`<project-name>-api.yaml`)
2. `doc-to-prd` -> PRD (`{project_name}_PRD.md`)
3. `prd-to-cli` -> generated CLI project

## Repository Structure

- `skills/api-to-doc/` - API URL/docs -> OpenAPI 3.0 YAML
- `skills/doc-to-prd/` - OpenAPI/docs -> PRD markdown
- `skills/prd-to-cli/` - PRD -> Python Click CLI scaffold
- `example_APIs/` - sample API specs/docs
- `example_PRDs/` - generated PRD examples
- `example_CLIs/` - generated CLI examples
- `docs/` - supporting documentation

## Workflow

### 1) API docs to OpenAPI

```bash
python skills/api-to-doc/scripts/fetch_api_info.py <url> --no-cache
```

Output artifact convention:
- `<project-name>-api.yaml`

### 2) OpenAPI to PRD

```bash
/doc-to-prd @<project-name>-api.yaml [output-path]
```

Output artifact convention:
- `{project_name}_PRD.md`

Notes:
- `project_name` is inferred from the spec/docs when possible.
- If it cannot be inferred confidently, provide it explicitly.
- Canonical PRD template used by this skill:
  - `skills/doc-to-prd/references/PRD_template.md`

### 3) PRD to CLI project

```bash
python skills/prd-to-cli/scripts/generate_cli_from_prd.py <prd_file> <output_dir> [project_name]
```

Generated project includes:
- `pyproject.toml`
- `Makefile`
- `src/config.py`, `src/logger.py`, `src/output.py`, `src/utils.py`
- `tests/test_cli.py`
- `requirements.txt`, `.env.example`

## Running Generated CLIs

Use CLI entry points with `uv`:

```bash
uv sync
uv run [cli-name] --help
uv run [cli-name] <resource> <command> [options]
```

Use this style in docs/examples/Makefiles:
- `uv run [cli-name] ...`
- `uv run $(PROJECT_NAME) ...`

Avoid this style in project docs:
- `uv run python -m src.cli ...`

## Testing

Inside a generated project:

```bash
uv run pytest tests/ -v
```

## Conventions

- Python 3.x, 4-space indentation, snake_case naming
- Keep generated outputs deterministic where possible
- Do not commit secrets; use `.env` and keep it git-ignored

## Example Artifacts

- API spec: `example_APIs/open-meteo/openapi.yaml`
- PRDs: `example_PRDs/`
- CLIs: `example_CLIs/`
