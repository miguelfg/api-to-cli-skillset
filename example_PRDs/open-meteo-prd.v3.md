# open-meteo Python Client - Product Requirements Document

## Document Metadata
- `project_name`: `open_meteo`
- `api_name`: `Open-Meteo API`
- `version`: `1.0.0`
- `base_url`: `https://api.open-meteo.com`
- `source_spec`: `example_APIs/open-meteo/openapi.yaml`
- `generated_on`: `2026-02-20`

## 1. Introduction
### Overview
Python CLI client for the Open-Meteo API to query weather and related forecast endpoints.

### Purpose
Provide a consistent command-line interface for endpoint access, batch execution, and export to JSON/CSV/XLSX.

### Target Audience
Python developers, data engineers, and automation users integrating weather data in scripts/pipelines.

### Key Capabilities
- Endpoint-oriented CLI commands
- Batch processing from CSV/TXT
- Export support for JSON, CSV, and XLSX

## 2. Installation
### Requirements
- Python: `>=3.10`
- Core dependencies:
  - `click>=8.0.0`
  - `requests>=2.28.0`

### Setup
```bash
uv sync
```

### Verify
```bash
uv run openmeteo-cli --help
```

## 3. Configuration
### Environment Variables
| Variable | Required | Description | Example |
|---|---|---|---|
| `OPEN_METEO_API_KEY` | No | API key if required by selected endpoint/provider | `your_api_key` |
| `OPEN_METEO_BASE_URL` | No | Override base URL | `https://api.open-meteo.com` |

### Config File
- Default path: `.env`
- Optional settings:
  - `timeout_seconds`: `30`
  - `max_retries`: `3`
  - `output_format`: `json`

## 4. Authentication
### Method
Primary endpoints are generally public; support optional API key auth in client configuration for provider-specific variants.

### Setup Steps
1. Create `.env` in project root
2. Set `base_url=https://api.open-meteo.com`
3. Optionally set API key/token fields if required by target endpoint

### Common Auth Errors
| Status/Code | Meaning | Resolution |
|---|---|---|
| `401` | Unauthorized | Verify key/token and header format |
| `403` | Forbidden | Check plan/permissions for provider endpoint |

## 5. Endpoint Reference
### Resource Naming
- Resources: `airquality, archive, bom, climate, cma, dmi, dwdicon, ecmwf, elevation, ensemble, flood, forecast, gem, gfs, jma, knmi, marine, meteofrance, metno, search`
- Command group convention: `open-meteo <resource> <operation>`

### Endpoint Inventory (GET)
- `/v1/air-quality`
- `/v1/archive`
- `/v1/bom`
- `/v1/climate`
- `/v1/cma`
- `/v1/dmi`
- `/v1/dwd-icon`
- `/v1/ecmwf`
- `/v1/elevation`
- `/v1/ensemble`
- `/v1/flood`
- `/v1/forecast`
- `/v1/gem`
- `/v1/gfs`
- `/v1/jma`
- `/v1/knmi`
- `/v1/marine`
- `/v1/meteofrance`
- `/v1/metno`
- `/v1/search`

## 6. CLI Design
### Command Structure
```text
open-meteo <resource> <command> [options]
```

### Standard Options
- `--output-format json|csv|xlsx`
- `--output-file <path>`
- `--verbose`
- `--dry-run`

### Batch Input (Optional)
- Supported formats: `csv, txt(json lines)`
- Example:
```bash
uv run openmeteo-cli batch --input-file data/batch.csv --format json --output-path ./output
```

## 7. Input/Output Examples
### Single Command Example
```bash
uv run openmeteo-cli forecast list --format json
```

### Example Output (JSON)
```json
{"data": {"temperature": 22.4, "wind_speed": 12.1}}
```

### Export Example
```bash
uv run openmeteo-cli forecast list --format xlsx --output-file output/forecast.xlsx
```

---

## Nice-to-Have: Caching
### Strategy
- Cache enabled by default: `false`
- TTL: `3600`
- Cache key strategy: `method + endpoint + query_hash`

## Nice-to-Have: Rate Limiting
### API Limits
- Documented limits: `TBD per endpoint/provider`

### Client Policy
- Retryable status codes: `408, 429, 500, 502, 503, 504`
- Backoff policy: `1s, 2s, 4s (+ jitter)`

## Nice-to-Have: Error Handling
### Error Classes
- Network errors: retry with exponential backoff
- Client errors: fail fast with actionable message
- Server errors: retry within max attempts
- Validation errors: return parameter-specific hints

## Nice-to-Have: Logging & Observability
### Logging Defaults
- Level: `INFO`
- Log destination: `stderr`
- Verbose mode behavior: request/response metadata + latency

## Nice-to-Have: Makefile & Project Management
### Suggested Targets
```makefile
install:
	uv sync

test:
	uv run pytest tests/ -v

run:
	uv run openmeteo-cli --help
```

### Typical Workflow
1. `uv sync`
2. `uv run openmeteo-cli --help`
3. `uv run openmeteo-cli <resource> <command> ...`

## Implementation Checklist (Quality Gates)
Use this checklist during implementation and review. These items were derived from issues observed in existing example CLIs.

- [ ] Do not shadow imported class/function names (for example, avoid redefining `Config` in a module that already imports `Config`).
- [ ] Ensure all advertised output formats are fully implemented (`json`, `csv`, `xlsx`) for both single commands and batch mode.
- [ ] Ensure batch request execution respects per-row HTTP method (`GET`, `POST`, `PUT/PATCH`, `DELETE`) instead of forcing one method.
- [ ] Avoid broad `except Exception`; catch expected exception types and return actionable user-facing errors.
- [ ] Use structured logging (and `click.echo` for CLI output) instead of raw `print()` in runtime paths.
- [ ] Parse `.env` defensively (skip malformed lines, comments, blank values) to avoid `split`/parse crashes.
- [ ] Define file I/O explicitly with encoding/newline policy (for example, UTF-8 and CSV-safe writes).
- [ ] Handle non-JSON/empty API responses safely before calling `.json()`.
- [ ] Keep authentication header names and auth schemes configurable per API (`X-API-Key`, `Authorization`, provider-specific headers).
- [ ] Validate and normalize base URL and endpoint joining to prevent malformed URLs.
- [ ] Avoid hidden placeholders like “format not yet implemented” in generated command handlers.
- [ ] Add coverage for error paths: auth failures, timeouts, retries exhausted, malformed batch rows, and invalid output paths.
- [ ] Add integration/smoke tests that verify generated files and CLI behavior end-to-end (not only `--help`/dry-run).
- [ ] Specify deterministic defaults for retry/backoff/timeouts and expose overrides via config/flags.
- [ ] Ensure generated project metadata is complete (`pyproject.toml`, console script entry point, dependencies).

## Open Questions
- Which Open-Meteo endpoints require provider-specific auth in your target usage?
- Which forecast models/resources are in scope for first release?
- What are expected batch input schema and output storage requirements?
