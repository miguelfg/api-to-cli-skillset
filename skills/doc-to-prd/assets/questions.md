# doc-to-prd Interactive Questions

Use these questions during PRD generation. Record answers under `## Implementation Decisions` in `{project_name}_PRD.md`.

Conventions:
- `[single-choice]` means choose exactly one option.
- `[multi-choice]` means choose one or more options.
- `[free-text]` means provide custom text.

## Project Identity

1. CLI name to run with `uv run <cli-name>` [free-text]
   - Example: `stripe-cli`

2. Python version target [single-choice]
   - `>=3.10` (Recommended)
   - `>=3.11`
   - `>=3.12`
   - custom [free-text]

## HTTP Stack

3. HTTP library [single-choice]
   - `requests` (Recommended)
   - `httpx`
   - `aiohttp`
   - `urllib3`

4. Retry/backoff policy [single-choice]
   - Enabled: `3 attempts`, `1s base`, `x2 backoff`, retry on `408,429,500,502,503,504` (Recommended)
   - Disabled
   - custom [free-text]

5. Timeout policy [single-choice]
   - `30s total timeout` (Recommended)
   - `60s total timeout`
   - custom [free-text]

## Authentication

6. Authentication scheme [single-choice]
   - `api_key` header (Recommended)
   - `bearer` token
   - `basic` auth
   - custom header/query [free-text]

7. Credential sources [multi-choice]
   - `.env` file (Recommended)
   - config file
   - CLI options

## CLI Behavior

8. Output formats [multi-choice]
   - `json` (Recommended)
   - `csv`
   - `xlsx`

9. Batch mode input formats [single-choice]
   - `csv + txt/jsonl` (Recommended)
   - `csv` only
   - `txt/jsonl` only
   - disabled

10. Timestamped output files [single-choice]
   - Yes, `%Y%m%d_%H%M%S` (Recommended)
   - No
   - custom format [free-text]

## Quality and Tooling

11. Lint/format toolchain [single-choice]
   - `ruff check --fix` + `ruff format` (Recommended)
   - `black` + `isort`
   - custom [free-text]

12. Required validation commands [multi-choice]
   - `make install` (Required)
   - `uv run <cli-name> --help` (Required)
   - `make <resource>-list` (Required)
   - additional checks [free-text]

## PRD Recording Template

Use this exact block in generated PRD:

```markdown
## Implementation Decisions

- CLI Name: `<cli-name>`
- Python Version: `<version-policy>`
- HTTP Library: `<requests|httpx|aiohttp|urllib3>`
- Authentication: `<scheme>`
- Credential Sources: `<.env|config|cli>`
- Timeout: `<seconds/policy>`
- Retry Policy: `<summary>`
- Output Formats: `<json,csv,xlsx>`
- Batch Input Formats: `<csv|txt|both|none>`
- Timestamped Outputs: `<yes/no + format>`
- Lint/Format Toolchain: `<ruff/...>`
- Validation Commands: `<commands>`
```
