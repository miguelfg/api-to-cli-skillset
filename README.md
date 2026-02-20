# API-to-CLI Skillset

Convert API docs/specs into Python CLI projects in three steps:

1. `api-to-doc` -> OpenAPI (`<project-name>-api.yaml`)
2. `doc-to-prd` -> PRD (`{project_name}_PRD.md`)
3. `prd-to-cli` -> generated CLI project

## Setup First

Before running the workflow, copy these skills into your local project under `skills/`:

- `skills/api-to-doc/`
- `skills/doc-to-prd/`
- `skills/prd-to-cli/`

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

Claude Code:

```bash
/api-to-doc <api-docs-url> [output-path]
```

Codex:

```bash
$api-to-doc <api-docs-url> [output-path]
```

### 2) OpenAPI to PRD

Claude Code:

```bash
/doc-to-prd <api-spec-path> [output-path]
```

Codex:

```bash
$doc-to-prd <api-spec-path> [output-path]
```

Notes:
- `project_name` is inferred from the spec/docs when possible.
- If it cannot be inferred confidently, provide it explicitly.
- Canonical PRD template used by this skill:
  - `skills/doc-to-prd/references/PRD_template.md`

### 3) PRD to CLI project

Claude Code:

```bash
/prd-to-cli <prd-file> <output-dir>
```

Codex:

```bash
$prd-to-cli <prd-file> <output-dir>
```

Generated project includes:
- `pyproject.toml`
- `Makefile`
- `src/config.py`, `src/logger.py`, `src/output.py`, `src/utils.py`
- `tests/test_cli.py`
- `requirements.txt`, `.env.example`

## Expected Artifacts

### Step 1: `api-to-doc`
- Artifact: OpenAPI YAML
- Naming convention: `<project-name>-api.yaml`
- Example: `example_APIs/stripe-api-v1-codex.yaml`

### Step 2: `doc-to-prd`
- Artifact: PRD markdown
- Naming convention: `{project_name}_PRD.md`
- Example: `example_PRDs/arkham_intel_api_PRD.md`

### Step 3: `prd-to-cli`
- Artifact: generated CLI project directory
- Naming convention: `<cli-name>/` (or provided output folder)
- Example: `example_CLIs/arkm-cli/`
- Common generated files:
  - `pyproject.toml`
  - `Makefile`
  - `src/cli.py`
  - `src/client.py`
  - `tests/test_cli.py`

## Running Generated CLIs

Use CLI entry points with `uv`:

```bash
cd <generated-project-dir>
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
