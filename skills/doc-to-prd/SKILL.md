---
name: doc-to-prd
description: Creates a comprehensive PRD (Product Requirements Document) for a Python API client based on a given API specification or documentation (online or offline). Generates structured markdown with installation, configuration, authentication, endpoint reference, caching, rate limiting, error handling, logging, and implementation decisions needed by prd-to-cli.
triggers:
  - User has an OpenAPI/Swagger file (local path or URL) and wants a `{project_name}_PRD.md` for a Python API client.
  - User asks to transform API documentation/specification into implementation-ready requirements.
  - User completed `api-to-doc` and needs the next artifact (`{project_name}_PRD.md`) before CLI generation.
do_not_trigger_when:
  mode: intent
  conditions:
    - Required input is missing (no API spec path/URL provided).
    - User intent is explanation, review, or discussion only (no artifact generation requested).
    - User asks directly for CLI code generation from an existing PRD (use `prd-to-cli` instead).
    - Request is ambiguous about target artifact and user has not confirmed intent.
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
- `OUTPUT_PATH` (optional): Path or directory where the generated `{project_name}_PRD.md` will be saved
  - Can be a filename: `my_api_PRD.md`
  - Can be a directory: `./docs/`, will create `{project_name}_PRD.md` inside
  - Default: `{project_name}_PRD.md` in current directory
  - If no explicit filename is provided, infer `project_name` from the API docs/spec; if not found, ask the user.
  - Example: `/doc-to-prd @openapi.yaml ./docs/stripe_PRD.md`

**Output:** Generated `{project_name}_PRD.md` file at specified location (or current directory if not specified)

---

## Overview

Creates a `{project_name}_PRD.md` file that gathers the API documentation in a structured format suitable for Python developers. Plus, it includes requests, response and code examples, usage guidelines, and best practices for integrating the API into Python applications. It also uses askUserQuestion tool to confirm user preferences, like:
  - preferred Python libraries for HTTP requests (e.g., requests, httpx, aiohttp)
  - full list of tackled enpoints
  - tackling batch requests
  - format saving responses (e.g., CSV, JSON, XSLX)
  - preferred authentication methods
  - logging practices
  - error handling strategies
  - performance optimization tips

Interactive prompt set:
- Use `assets/questions.md` as the canonical questionnaire for this skill.
- Persist user answers in a dedicated PRD section (for example `## Implementation Decisions`), so `prd-to-cli` can generate code without asking again.

Its workflow would follow:
- Gather API documentation from the provided source (URL or file).
- Extract relevant information such as endpoints, methods, parameters, and data formats.
- Structure the information into sections relevant for Python developers.
- Include code snippets and examples using popular Python libraries (e.g., requests, httpx).
- Format the generated PRD file with clear headings, bullet points, and tables for easy reference.

Project name resolution for output filename:
- Try to extract `project_name` from API documentation/spec first (for example `info.title`, API/product title, or service name in docs headings).
- Normalize to a filesystem-safe slug (lowercase, spaces/special chars converted to `_`).
- If `project_name` cannot be determined with confidence, ask the user for it before writing output.

Do not hardcode implementation defaults in this skill.
- Capture preferences/decisions from user answers in `assets/questions.md`.
- Record final choices in PRD so `prd-to-cli` treats them as source of truth.
- Keep content implementation-neutral where user has not explicitly decided.

Don't:
- Include any actual code implementation of the API client.
- Write other documentation files beyond `{project_name}_PRD.md`.
- Assume any specific API structure; adapt to the provided documentation, otherwise ask the user for clarifications.
- Generate unit tests or other testing frameworks.
- Create deployment scripts or CI/CD pipelines.

---

## PRD Template Structure

The skill generates `{project_name}_PRD.md` files using a single canonical template:
`references/PRD_template.md`.

### PRD Sections

Core sections:
1. **Introduction** - Overview, purpose, audience, key capabilities
2. **Installation** - Requirements and setup steps
3. **Configuration** - Environment variables and config strategy
4. **Authentication** - Auth method(s), setup, and failure modes
5. **Endpoint Reference** - Resource-by-resource endpoint details
6. **CLI Design** - Command groups and standard options
7. **Input/Output Examples** - Typical request/response and output formatting

Nice-to-have sections:
1. **Caching** - Strategy, TTL, and cache controls
2. **Rate Limiting** - Limits, retries, and backoff policy
3. **Error Handling** - Error classes and user-facing guidance
4. **Logging & Observability** - Log levels and debugging behavior
5. **Makefile & Project Management** - Local workflows and automation

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

`doc-to-prd` should only define a consumer contract, not implementation details.

Required contract to include in PRD:
- Runtime commands must use `uv run [cli-name] ...`
- Generated CLI should be installable with `uv sync`
- `prd-to-cli` owns final Makefile targets, dependency pins, and packaging details

---

## Output Example: Generated {project_name}_PRD.md Structure

When the skill generates `{project_name}_PRD.md`, it follows this structure:

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
[doc-to-prd] → {project_name}_PRD.md (comprehensive, this skill)
  ↓
[prd-to-cli] → Python Click CLI Project
  ↓
[Makefile] → Manage, test, deploy
```

---

## Usage Tips

### Customizing the Template

After generating `{project_name}_PRD.md`, customize for your API:

1. Replace placeholders: `[API Name]`, `[cli-name]`, `[RESOURCE_NAME]`
2. Update rate limits and authentication details
3. Add API-specific configuration options
4. Customize Makefile for your project structure
5. Add project-specific logging or caching requirements

### Best Practices

✓ Review generated `{project_name}_PRD.md` carefully
✓ Update examples with real API values
✓ Test all endpoint examples before finalizing
✓ Keep `{project_name}_PRD.md` in sync with implementation
✓ Use version control for `{project_name}_PRD.md` changes
✓ Include `{project_name}_PRD.md` in project documentation
✓ Reference `{project_name}_PRD.md` in README.md

---

## References

- **[PRD_template.md](references/PRD_template.md)** - Canonical template used by `doc-to-prd`
- Related skills: `prd-to-cli`, `api-to-doc`

## Next Possible Steps

Run skills in sequence from this stage:

1. Generate CLI project from your PRD:
```bash
/prd-to-cli @{project_name}_PRD.md <output-folder>
```
2. If PRD content is incomplete, regenerate or refine upstream inputs:
```bash
/api-to-doc <api-docs-url> [output-folder]
```
