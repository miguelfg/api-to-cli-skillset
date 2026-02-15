---
name: api-to-doc
description: Convert API URLs and documentation into OpenAPI 3.0.0 YAML specifications. Auto-detects API type (existing OpenAPI specs, Swagger, REST HTML documentation), extracts endpoints using cURL-based intelligent parsing, and generates structured specifications. Use when you have an API URL and need to create an OpenAPI YAML file for use with doc-to-prd to generate API client PRDs.
---

# API to OpenAPI Generator

## Overview

The **api-to-doc** skill converts API URLs into standardized OpenAPI 3.0.0 YAML specifications. It intelligently fetches and parses API documentation from URLs, automatically extracts HTTP endpoints and metadata, and generates well-formed OpenAPI specs without manual boilerplate writing.

**Key features:**
- Auto-detect OpenAPI specs, Swagger, or HTML documentation
- Extract endpoints using intelligent pattern matching
- Fallback to interactive Q&A for complex or minimal documentation
- Generate valid OpenAPI 3.0.0 YAML output
- First step in the api-to-cli workflow

## Expected Parameters

```
/api-to-doc <API_URL> [OUTPUT_FOLDER]
```

**Parameters:**
- `API_URL` (required): The URL to API documentation or an endpoint serving OpenAPI/Swagger spec
  - Examples: `https://petstore.swagger.io`, `https://api.github.com/docs`, `https://api.example.com`
- `OUTPUT_FOLDER` (optional): Directory where the generated `openapi.yaml` will be saved
  - Default: Current working directory
  - Example: `/api-to-doc https://api.example.com ./specs`

## Workflow

### 1. Provide an API URL

Pass the API documentation URL to the skill:

```
/api-to-doc https://example-api.com/docs
/api-to-doc https://petstore.swagger.io
```

### 2. Auto-Detection

The skill attempts to:

1. **Fetch the URL** using cURL (handles redirects, follows links)
2. **Detect API type:**
   - If it's already an OpenAPI/Swagger JSON/YAML → Extract directly
   - If it's HTML documentation → Parse for HTTP endpoints
   - If unclear → Fall back to interactive mode
3. **Extract endpoints** using regex patterns for common documentation formats
4. **Identify base URL** from content or request URL

### 3. Interactive Mode (If Needed)

If auto-detection finds few or no endpoints, the skill prompts interactively:

```
=== API Configuration ===
API Title: My API
API Version: 1.0.0
Base URL: https://api.example.com
Description: (optional)

=== Define Endpoints ===
Method: GET
Path: /users
Description: List users
Tag: Users
```

### 4. Generate OpenAPI YAML

Output a valid OpenAPI 3.0.0 file with:
- Info section (title, version, description)
- Server configuration
- All extracted endpoints with methods, paths, and tags
- Response definitions
- Parameter extraction (path variables, query params)

## Usage Examples

### Example 1: Existing OpenAPI Spec

```bash
/api-to-doc https://petstore.swagger.io
```

**Result:** Converts Swagger/OpenAPI to standard OpenAPI 3.0 YAML

### Example 2: HTML REST Documentation

```bash
/api-to-doc https://api.github.com/docs
```

**Result:** Parses HTML documentation, extracts endpoints like:
- `GET /repos/{owner}/{repo}`
- `POST /repos/{owner}/{repo}/issues`
- `GET /repos/{owner}/{repo}/pulls`

### Example 3: Interactive Definition

```bash
/api-to-doc https://internal-api.company.com
# → Auto-detection finds no endpoints
# → Switches to interactive mode
# → User defines: 3-5 endpoints manually
# → Generates OpenAPI YAML
```

## Understanding the Output

Generated `openapi.yaml` structure:

```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /users:
    get:
      summary: List users
      tags:
        - Users
      responses:
        '200':
          description: Successful response
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
```

For detailed OpenAPI structure reference, see [openapi_structure.md](references/openapi_structure.md).

## How API Detection Works

### Swagger/OpenAPI Detection

If the content contains `"openapi"` or `"swagger"` keys, it's treated as an existing spec and converted to OpenAPI 3.0.0.

### HTML Documentation Pattern Recognition

The skill searches for HTTP method + path patterns like:

```
GET /api/users
POST /users/{id}
DELETE /endpoint
```

For detailed documentation patterns and extraction strategies, see [doc_patterns.md](references/doc_patterns.md).

### Fallback: Interactive Mode

If patterns don't match, ask the user to define endpoints manually. This ensures no API is left unsupported.

## Configuration & Customization

### Base URL Detection

The skill looks for base URL indicators in the fetched content:

- Meta tags: `<meta name="api-base-url" content="https://api.example.com">`
- Documentation text: `Base URL: https://api.example.com`
- JavaScript constants: `const API_BASE = "https://api.example.com"`

If not found, defaults to the domain of the provided URL.

### Endpoint Tagging

Endpoints are automatically tagged by resource type (Users, Posts, Comments, etc.) based on the path structure. Tags help organize endpoints in the generated PRD.

### Response Schemas

Generated responses use minimal but valid JSON schema:

```yaml
responses:
  '200':
    description: Successful response
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: object
```

Users can enhance these in the generated OpenAPI file or in the PRD step.

## Next Steps

Once you have an `openapi.yaml` file:

```bash
/doc-to-prd @openapi.yaml
```

This converts the OpenAPI spec into a comprehensive PRD.md with authentication, examples, and best practices—ready for the next step: `prd-to-cli`.

## Troubleshooting

### No endpoints extracted

**Causes:**
- Website uses JavaScript rendering (cURL can't execute JS)
- Documentation in non-standard format
- Anti-bot protection blocks cURL

**Solution:** Use interactive mode to manually define endpoints

### Base URL detection fails

**Causes:**
- Base URL in JavaScript or external config
- Multiple server environments (dev/staging/prod)

**Solution:** Edit the generated YAML manually or specify in interactive mode

### Some endpoints missing

**Causes:**
- Documentation uses non-standard HTTP method notation
- Endpoints hidden behind expandable sections

**Solution:** Add missing endpoints manually to generated YAML

## References

- **[openapi_structure.md](references/openapi_structure.md)** — OpenAPI 3.0.0 schema and structure guide
- **[doc_patterns.md](references/doc_patterns.md)** — API documentation patterns and extraction strategies
- **[examples.md](references/examples.md)** — Real-world examples and workflow demonstrations
