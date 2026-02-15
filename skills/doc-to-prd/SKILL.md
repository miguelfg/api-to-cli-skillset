---
name: doc-to-prd
description: Creates a PRD for a Python API client based on a given API specification or documentation (online or offline).
---

## Expected Parameters

```
/doc-to-prd <API_SPEC_PATH> [OUTPUT_PATH]
```

**Parameters:**
- `API_SPEC_PATH` (required): Path to API specification file
  - Accepts OpenAPI YAML/JSON files (e.g., `openapi.yaml`, `swagger.json`)
  - Can be a file path or URL to an OpenAPI spec
  - Example: `/doc-to-prd @openapi.yaml` or `/doc-to-prd https://api.example.com/openapi.json`
- `OUTPUT_PATH` (optional): Path or directory where the generated `PRD.md` will be saved
  - Can be a filename: `PRD.md`, `my-api-prd.md`
  - Can be a directory: `./docs/`, will create `PRD.md` inside
  - Default: `PRD.md` in current directory
  - Example: `/doc-to-prd @openapi.yaml ./docs/my-api-prd.md`

**Output:** Generated `PRD.md` file at specified location (or current directory if not specified)

---

## Overview

Creates a PRD.md file that gathers the API documentation in a structured format suitable for Python developers. Plus, it includes requests, response and code examples, usage guidelines, and best practices for integrating the API into Python applications. It also uses askUserQuestion tool to confirm user preferences, like:
  - preferred Python libraries for HTTP requests (e.g., requests, httpx, aiohttp)
  - full list of tackled enpoints
  - tackling batch requests
  - format saving responses (e.g., CSV, JSON, XSLX)
  - preferred authentication methods
  - logging practices
  - error handling strategies
  - performance optimization tips

Its workflow would follow:
- Gather API documentation from the provided source (URL or file).
- Extract relevant information such as endpoints, methods, parameters, and data formats.
- Structure the information into sections relevant for Python developers.
- Include code snippets and examples using popular Python libraries (e.g., requests, httpx).
- Format the PRD.md file with clear headings, bullet points, and tables for easy reference.

By default, the PRD.md file will include this design decisions to a later developing of the PRD.md:
- Use of the `requests` library for HTTP requests.
- JSON as the primary data format for requests and responses.
- Basic authentication methods (e.g., API keys, OAuth2).
- Error handling using try-except blocks with error classification:
  - Network errors (ConnectionError, Timeout, HTTP 5xx): Retry with exponential backoff
  - Client errors (HTTP 4xx except 429): Display error message, don't retry
  - Data errors (validation failures): Raise exception with details
- Retry logic with exponential backoff:
  - Max attempts: 3
  - Initial delay: 1 second
  - Backoff multiplier: 2 (1s → 2s → 4s)
  - Jitter: ±10% randomization to avoid thundering herd
  - Retriable status codes: 408, 429, 500, 502, 503, 504
- Connection pooling for performance:
  - Use `requests.Session()` for persistent connections
  - Pool size: 10 connections
  - Timeout: 30 seconds per request
  - HTTPAdapter with pool_connections and pool_maxsize configuration
- API courtesy practices:
  - Add 100ms delay between requests to public APIs
  - Respect cache to minimize API calls
  - Log all requests for auditing
  - Implement rate limit detection (429 responses)
- Logging using the built-in `logging` module:
  - Log levels: DEBUG, INFO (default), WARNING, ERROR
  - Log format with timestamps, operation summaries, cache indicators, execution duration
  - Separate logs for queries, errors, and cache operations
  - Debug mode (--verbose) shows full request/response payloads and stack traces
- Configuration file management:
  - Store settings in `.{tool_name}_settings.json` (in same directory as CLI module)
  - Default configuration template: see `templates/default_config.json` in this skill
  - Allow users to override defaults via config commands (set, show, reset)
- Develop the API client as CLI tool with `click`:
  - CLI structure using click groups for complex command hierarchies:
    - Root command group for main entry point
    - Subcommand groups for logical operations (e.g., query, export, metadata, cache, config)
    - Commands nested under subgroups (e.g., `query payments`, `query recipients`, `export payments`)
    - Each endpoint typically corresponds to a click subcommand
  - Command design:
    - Prioritize click options over arguments (better discoverability via --help)
    - Pattern: `tool-name subgroup command --option value` not `tool-name subgroup command value`
    - Add skip and limit options for endpoints returning large datasets
    - Add dry-run option to simulate requests without executing
    - Add --override option to bypass cache and fetch fresh data
    - Add --verbose flag for debug-level output
  - Default behavior:
    - Check if data is already cached before making requests
    - Support multiple output formats (--format json|csv|xlsx)
    - Include --output-file option to save results to file
  - Cache integration:
    - Cache key: hash of query parameters
    - Include cache management subgroup (list, clear, info, delete commands)
- Use Pandas for data manipulation and storage when dealing with tabular data:
  - with utf-8 encoding by default
  - on csv ouput, format floats with 0 decimal places
  - don't include the index column when saving dataframes to files

Don't:
- Include any actual code implementation of the API client.
- Write other documentation files beyond PRD.md.
- Assume any specific API structure; adapt to the provided documentation, otherwise ask the user for clarifications.
- Generate unit tests or other testing frameworks.
- Create deployment scripts or CI/CD pipelines.

