---
name: doc-to-prd
description: Creates a comprehensive PRD (Product Requirements Document) for a Python API client based on a given API specification or documentation (online or offline). Generates structured markdown with installation, configuration, authentication, endpoint reference, caching, rate limiting, error handling, logging, best practices, and Makefile/uvicorn integration guidance.
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

---

## PRD Template Structure

The skill generates PRD.md files following a comprehensive template that includes all necessary sections for API client development. See the template in `references/PRD_template.md`.

### PRD Sections

1. **Introduction** - Overview, purpose, target audience, key features
2. **Installation** - System requirements, installation methods, dependencies, verification
3. **Configuration** - Environment variables, config files, configuration management commands
4. **Authentication** - API key setup, authentication methods, error handling, best practices
5. **Endpoint Reference** - Resource documentation with method, path, parameters, response, examples
   - Subsections for each API resource (Users, Posts, Comments, etc.)
   - Standard CRUD operations (List, Get, Create, Update, Delete)
6. **Input/Output Examples** - Single request and batch processing examples with outputs in various formats
7. **Caching** - Overview, configuration, management commands, strategy, best practices
8. **Rate Limiting** - API limits, client-side rate limiting, configuration, example handling
9. **Error Handling** - Error classification, response format, common errors with solutions
10. **Logging** - Log levels, configuration, log format, verbose mode, best practices
11. **Best Click Practices** - CLI design principles, standard options, error messages, performance
12. **Makefile & Project Management** - Project structure, Makefile commands, uvicorn integration

### Template Customization

The template uses placeholders for easy customization:

- `[API Name]` - Your API name
- `[api-prefix]` - API environment variable prefix (e.g., STRIPE, GITHUB)
- `[cli-name]` - CLI tool name (e.g., stripe-cli, github-cli)
- `[RESOURCE_NAME]` - API resource names (e.g., users, posts)
- `[Limit]` - Rate limit values
- `[org]` - Organization/company name

---

## Makefile & Project Management

### Makefile Integration

The generated PRD.md includes a sample Makefile with common development tasks:

**Standard Makefile Targets:**

```bash
make install          # Install in development mode
make install-dev      # Install with dev dependencies
make lint             # Run code linting
make format           # Format code
make test             # Run unit tests
make test-cov         # Run tests with coverage
make dev              # Start development environment
make build            # Build distribution packages
make clean            # Clean build artifacts
make docs             # Generate documentation
make prd              # Generate/update PRD.md
make serve            # Run development server with uvicorn
make serve-prod       # Run production server with uvicorn
```

**Example Makefile for Click CLI:**

```makefile
.PHONY: help install test lint format

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	flake8 src/ && pylint src/

format:
	black src/ && isort src/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src/

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	python -m build

prd:
	@echo "PRD.md is maintained in documentation/"
```

### uvicorn Integration

The PRD recommends **uvicorn** as the optional CLI project management and development server tool.

**When to use uvicorn:**

- Development server for testing API client functionality
- Running local mock API for testing
- Serving documentation or admin endpoints
- Integration with async/ASGI features (future enhancement)

**Installation:**

```bash
pip install uvicorn
```

**Basic Usage:**

```bash
# Run development server
uvicorn [cli_name].server:app --reload --port 8000

# Run with specific settings
uvicorn [cli_name].server:app --host 0.0.0.0 --port 8000 --workers 4

# Run with configuration file
uvicorn [cli_name].server:app --config uvicorn.ini
```

**Makefile Integration:**

```makefile
serve:
	uvicorn [cli_name].server:app --reload --port 8000

serve-prod:
	uvicorn [cli_name].server:app --host 0.0.0.0 --port 8000 --workers 4

serve-debug:
	uvicorn [cli_name].server:app --reload --port 8000 --log-level debug
```

**Configuration File (uvicorn.ini):**

```ini
[server]
host = 0.0.0.0
port = 8000
workers = 4
reload = true
log-level = info
```

**Use Cases for uvicorn with Click CLI:**

1. **Development Server** - Test CLI against local mock API
2. **Documentation Server** - Serve auto-generated API documentation
3. **Admin Interface** - Provide web UI for configuration management
4. **Health Checks** - Expose `/health` endpoint for monitoring
5. **Telemetry** - Serve metrics endpoint for monitoring tools

---

## Output Example: Generated PRD.md Structure

When the skill generates a PRD.md, it follows this structure:

```markdown
# API Python Client - Product Requirements Document

## Table of Contents
1. Introduction
2. Installation
3. Configuration
...

## Introduction
### Overview
### Purpose
### Target Audience
### Key Features

## Installation
### System Requirements
### Installation Methods
### Verify Installation
### Dependencies

## Configuration
### Environment Variables
### Configuration File
### Configuration Management Commands

## Authentication
### API Key Authentication
### Authentication Methods
### Error Handling
### Best Practices

## Endpoint Reference
### Resource Naming
### Endpoint Structure
### [RESOURCE_NAME]
#### List [Resource]
#### Get [Resource]
#### Create [Resource]
#### Update [Resource]
#### Delete [Resource]

## Input/Output Examples
### Single Request Examples
### Batch Processing Examples
### Output Format Examples

## Caching
### Overview
### Configuration
### Management Commands
### Best Practices

## Rate Limiting
### API Rate Limits
### Client Rate Limiting
### Configuration
### Best Practices

## Error Handling
### Error Classification
### Error Response Format
### Common Errors
### Best Practices

## Logging
### Log Levels
### Configuration
### Log Format
### Best Practices

## Best Click Practices
### CLI Command Design
### Standard Options
### Error Messages
### Performance Best Practices

## Makefile & Project Management
### Project Structure
### Makefile Commands
### uvicorn Integration
### Common Workflow
```

---

## Integration with api-to-cli Workflow

The `doc-to-prd` skill fits into the complete workflow:

```
API URL
  ↓
[api-to-doc] → OpenAPI YAML/JSON
  ↓
[doc-to-prd] → PRD.md (comprehensive, this skill)
  ↓
[prd-to-cli] → Python Click CLI Project
  ↓
[Makefile] → Manage, test, deploy
```

---

## Usage Tips

### Customizing the Template

After generating PRD.md, customize for your API:

1. Replace placeholders: `[API Name]`, `[cli-name]`, `[RESOURCE_NAME]`
2. Update rate limits and authentication details
3. Add API-specific configuration options
4. Customize Makefile for your project structure
5. Add project-specific logging or caching requirements

### Best Practices

✓ Review generated PRD.md carefully
✓ Update examples with real API values
✓ Test all endpoint examples before finalizing
✓ Keep PRD.md in sync with implementation
✓ Use version control for PRD.md changes
✓ Include PRD.md in project documentation
✓ Reference PRD.md in README.md

---

## References

- **[PRD_template.md](references/PRD_template.md)** - Complete PRD template with all sections
- Related skills: `prd-to-cli`, `api-to-doc`

