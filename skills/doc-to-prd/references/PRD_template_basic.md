# {project_name} Python Client - Product Requirements Document

## Document Metadata
- `project_name`: `{project_name}`
- `api_name`: `{api_name}`
- `version`: `{version}`
- `base_url`: `{base_url}`
- `source_spec`: `{source_spec_or_url}`
- `generated_on`: `{generated_date}`

## 1. Introduction
### Overview
{overview}

### Purpose
{purpose}

### Target Audience
{target_audience}

### Key Capabilities
- {capability_1}
- {capability_2}
- {capability_3}

## 2. Installation
### Requirements
- Python: `{python_version}`
- Core dependencies:
  - `{dependency_1}`
  - `{dependency_2}`

### Setup
```bash
{install_commands}
```

### Verify
```bash
{verify_commands}
```

## 3. Configuration
### Environment Variables
| Variable | Required | Description | Example |
|---|---|---|---|
| `{api_prefix}_API_KEY` | Yes | API key for authentication | `{api_key_example}` |
| `{api_prefix}_BASE_URL` | No | Override default API base URL | `{base_url}` |

### Config File
- Default path: `{config_file_path}`
- Optional settings:
  - `timeout_seconds`: `{timeout_seconds}`
  - `max_retries`: `{max_retries}`
  - `output_format`: `{default_output_format}`

## 4. Authentication
### Method
{auth_method}

### Setup Steps
1. {auth_step_1}
2. {auth_step_2}
3. {auth_step_3}

### Common Auth Errors
| Status/Code | Meaning | Resolution |
|---|---|---|
| `{auth_error_code_1}` | {auth_error_meaning_1} | {auth_error_fix_1} |
| `{auth_error_code_2}` | {auth_error_meaning_2} | {auth_error_fix_2} |

## 5. Endpoint Reference
### Resource Naming
- Resources: `{resource_list_csv}`
- Command group convention: `{cli_name} <resource> <operation>`

### Resource: `{resource_name_1}`
#### List
- Method: `GET`
- Path: `/{resource_path_1}`
- Query params: `{list_query_params}`
- Success response: `{list_response_shape}`

#### Get
- Method: `GET`
- Path: `/{resource_path_1}/{id_param}`
- Path params: `{id_param}`
- Success response: `{get_response_shape}`

#### Create
- Method: `POST`
- Path: `/{resource_path_1}`
- Body schema: `{create_body_schema_summary}`
- Success response: `{create_response_shape}`

#### Update
- Method: `PUT|PATCH`
- Path: `/{resource_path_1}/{id_param}`
- Body schema: `{update_body_schema_summary}`
- Success response: `{update_response_shape}`

#### Delete
- Method: `DELETE`
- Path: `/{resource_path_1}/{id_param}`
- Success response: `{delete_response_shape}`

## 6. CLI Design
### Command Structure
```text
{cli_name} <resource> <command> [options]
```

### Standard Options
- `--output-format {output_formats}` (default: `{default_output_format}`)
- `--output-file <path>`
- `--verbose`
- `--dry-run` (if supported)

### Batch Input (Optional)
- Supported formats: `{batch_formats}`
- Example:
```bash
{batch_example_command}
```

## 7. Input/Output Examples
### Single Command Example
```bash
{single_example_command}
```

### Example Output (JSON)
```json
{single_example_output_json}
```

### Export Example
```bash
{export_example_command}
```

---

## Nice-to-Have: Caching
### Strategy
- Cache enabled by default: `{cache_enabled}`
- TTL: `{cache_ttl}`
- Cache key strategy: `{cache_key_strategy}`

### Cache Commands (If Implemented)
```bash
{cache_commands}
```

## Nice-to-Have: Rate Limiting
### API Limits
- Documented limits: `{rate_limit_values}`

### Client Policy
- Retryable status codes: `{retryable_codes}`
- Backoff policy: `{backoff_policy}`

## Nice-to-Have: Error Handling
### Error Classes
- Network errors: `{network_error_handling}`
- Client errors: `{client_error_handling}`
- Server errors: `{server_error_handling}`
- Validation errors: `{validation_error_handling}`

## Nice-to-Have: Logging & Observability
### Logging Defaults
- Level: `{log_level}`
- Log destination: `{log_destination}`
- Verbose mode behavior: `{verbose_behavior}`

## Nice-to-Have: Makefile & Project Management
### Suggested Targets
```makefile
{makefile_targets}
```

### Typical Workflow
1. `{workflow_step_1}`
2. `{workflow_step_2}`
3. `{workflow_step_3}`

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
- {open_question_1}
- {open_question_2}
- {open_question_3}
