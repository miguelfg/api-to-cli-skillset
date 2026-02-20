---
name: api-to-doc
description: Convert API URLs and documentation into comprehensive OpenAPI 3.0.0 YAML specifications. Auto-detects API type (existing OpenAPI specs, Swagger, REST HTML documentation), intelligently extracts endpoints with complete parameter documentation (path, query, body), request/response examples using HTML parsing and pattern matching, and generates well-structured specifications. Falls back to Playwright or WebFetch when cURL is insufficient. Use when you have an API URL and need to create an OpenAPI YAML file for use with doc-to-prd to generate API client PRDs.
triggers:
  - User provides an API docs URL, API base URL, or Swagger/OpenAPI endpoint and wants an OpenAPI spec.
  - User asks to convert HTML API docs into an OpenAPI YAML file.
  - User is starting the API-to-CLI workflow and needs the first artifact (`<project-name>-api.yaml`).
do_not_trigger_when:
  mode: intent
  conditions:
    - Required input is missing (no API URL/docs URL/spec endpoint provided).
    - User intent is explanation, review, or discussion only (no artifact generation requested).
    - User already has a valid OpenAPI file and asks for a later pipeline step (PRD/CLI generation).
    - Request is ambiguous about target artifact and user has not confirmed intent.
---

# API to OpenAPI Generator

## Overview

The **api-to-doc** skill converts API URLs into standardized OpenAPI 3.0.0 YAML specifications. It intelligently fetches and parses API documentation from URLs, automatically extracts HTTP endpoints and metadata, and generates well-formed OpenAPI specs without manual boilerplate writing.

**Key features:**
- Auto-detect OpenAPI specs, Swagger, or HTML documentation
- Extract endpoints with complete parameter documentation (path, query, body parameters)
- Intelligently parse request/response examples from code blocks
- Extract parameter types and required/optional status
- Fallback to Playwright or WebFetch when cURL returns incomplete results
- HTML parsing with tag extraction and structure analysis
- Fallback to interactive Q&A for complex or minimal documentation
- Generate valid OpenAPI 3.0.0 YAML with enhanced schema information
- First step in the api-to-cli workflow

## Expected Parameters

```
/api-to-doc <API_URL> [OUTPUT_FOLDER]
```

**Parameters:**
- `API_URL` (required): The URL to API documentation or an endpoint serving OpenAPI/Swagger spec
  - Examples: `https://petstore.swagger.io`, `https://api.github.com/docs`, `https://api.example.com`
- `OUTPUT_FOLDER` (optional): Directory where the generated `<project-name>-api.yaml` file will be saved
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

Generated `<project-name>-api.yaml` structure:

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

The generated spec now includes:
- **Path Parameters**: Extracted from URL patterns (e.g., `{id}`, `:id`)
- **Query Parameters**: Parsed from documentation sections like "Query Parameters" or "Optional Parameters"
- **Request Body**: Extracted from "Request Body" sections or inferred from example JSON
- **Response Schemas**: Generated from "Response Example" sections when available
- **Parameter Types**: Inferred from documentation patterns (string, integer, object, etc.)
- **Required/Optional Status**: Detected from documentation language

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

Additionally, it extracts:
- **Path Parameters**: From `{id}`, `:id`, `[id]` patterns in URLs
- **Query Parameters**: From "Query Parameters" sections or inline patterns
- **Body Parameters**: From "Request Body" or "Payload" sections
- **Examples**: From code blocks marked "Request Example", "Response Example"

For detailed documentation patterns and extraction strategies, see [doc_patterns.md](references/doc_patterns.md).

### Fallback: MCP-Based Extraction (When cURL is Insufficient)

If cURL returns incomplete or empty results:
1. The skill notes this in the output
2. Recommendations are provided to use browser-based extraction
3. Consider using Playwright skill (webapp-testing) to render JavaScript-heavy docs
4. Or use WebFetch/WebSearch for additional context gathering

### Fallback: Interactive Mode

If patterns don't match or additional endpoints are needed, the skill falls back to interactive Q&A where users define endpoints manually. This ensures no API is left unsupported.

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

Once you have a `<project-name>-api.yaml` file:

```bash
/doc-to-prd @<project-name>-api.yaml
```

This converts the OpenAPI spec into a comprehensive PRD.md with authentication, examples, and best practices—ready for the next step: `prd-to-cli`.

## Troubleshooting

### No endpoints extracted

**Causes:**
- Website uses JavaScript rendering (cURL can't execute JS)
- Documentation in non-standard format
- Anti-bot protection blocks cURL

**Solutions:**
1. Skill will recommend browser-based extraction
2. Use Playwright (webapp-testing skill) to render the page first
3. Use WebFetch for alternative content fetching
4. Fall back to interactive mode for manual definition

### Incomplete parameter extraction

**Causes:**
- Parameters documented in images or diagrams
- Documentation uses non-standard terminology ("args", "fields", etc.)
- Parameters in external files or separate pages

**Solutions:**
1. Edit the generated OpenAPI YAML to add missing parameters
2. Use browser-based extraction for more complete access
3. Manually enhance parameters in the interactive PRD step

### Request/Response examples not extracted

**Causes:**
- Examples in JavaScript objects (not JSON)
- Examples in custom code block syntax
- Examples in HTML tables without code formatting

**Solutions:**
1. Examples can be added during the PRD generation step
2. Edit the OpenAPI spec to add `example` and `examples` properties
3. Consider providing raw API test examples in the PRD

### Base URL detection fails

**Causes:**
- Base URL in JavaScript or external config
- Multiple server environments (dev/staging/prod)

**Solution:** Edit the generated YAML manually or specify in interactive mode

### Some endpoints missing

**Causes:**
- Documentation uses non-standard HTTP method notation
- Endpoints hidden behind expandable sections or tabs
- JavaScript-rendered navigation required

**Solutions:**
1. Add missing endpoints manually to generated YAML
2. Use browser-based extraction to access all documentation
3. Use interactive mode to add additional endpoints

## Advanced Features

### HTML Content Parsing

The skill includes an `HTMLContentExtractor` class that:
- Parses HTML structure for better context understanding
- Extracts text content and code blocks separately
- Identifies section headers (h1-h5) for better organization
- Handles nested elements and preserves meaningful whitespace

This enables more accurate extraction of parameter documentation and examples.

### Parameter Extraction

**Path Parameters:** Automatically extracted from endpoint URLs using patterns like `{id}`, `:id`, `[id]`

**Query Parameters:** Located by searching for documentation sections containing:
- "Query Parameters"
- "Query String"
- "Optional Parameters"
- "Parameters"

**Request Body:** Located by searching for sections containing:
- "Request Body"
- "Body Parameters"
- "Payload"
- "Body"

**Inferred from Examples:** When explicit documentation is missing, types and required status are inferred from code examples.

### Example and Schema Extraction

The skill automatically extracts:
- **Request Examples**: From markdown/HTML code blocks labeled "Request Example"
- **Response Examples**: From code blocks labeled "Response Example"
- **Schema Generation**: Uses examples to infer field types and object structures
- **JSON Parsing**: Validates extracted examples as valid JSON before including

## HTML Caching & Crawling

The skill now includes advanced HTML management for comprehensive API documentation extraction:

### HTML Caching to `/tmp`

All fetched documentation pages are automatically saved to:
```
/tmp/api-to-doc-cache/
```

**Files are cached by default** to enable:
- Inspection and debugging of fetched content
- Link extraction for multi-page crawling
- Offline analysis of documentation
- Performance optimization for repeated requests

**Disable caching:**
```bash
python scripts/fetch_api_info.py <url> --no-cache
```

### Link Extraction

The `link_extractor.py` helper identifies crawlable API documentation pages:

```bash
python scripts/link_extractor.py <html_file> <base_url> [output.json]
```

**Categorizes links into:**
- api_docs, endpoints, reference, guides, auth, examples, other

**Filters by:**
- Same domain only
- Excludes search, pagination, blogs, forums
- Path depth ≤ 2 levels by default

### Multi-Page Crawling

The `crawler.py` script discovers all API endpoints across multiple pages:

```bash
# Crawl up to 10 pages
python scripts/crawler.py <start_url>

# Crawl more pages
python scripts/crawler.py <start_url> 25 2
```

**Crawl workflow:**
1. Fetch page → Extract endpoints → Find links
2. Filter links → Queue crawlable pages
3. Repeat until max pages reached

**Output:** Complete list of endpoints discovered across entire documentation

For detailed crawling guide, see [crawling_guide.md](references/crawling_guide.md).

## References

- **[openapi_structure.md](references/openapi_structure.md)** — OpenAPI 3.0.0 schema and structure guide
- **[doc_patterns.md](references/doc_patterns.md)** — API documentation patterns and extraction strategies (now includes parameter patterns!)
- **[crawling_guide.md](references/crawling_guide.md)** — HTML caching, link extraction, and multi-page crawling guide
- **[examples.md](references/examples.md)** — Real-world examples and workflow demonstrations

## Next Possible Steps

Run skills in sequence after this step:

1. Generate PRD from your spec:
```bash
/doc-to-prd @<project-name>-api.yaml
```
2. Generate CLI project from PRD:
```bash
/prd-to-cli @PRD.md <output-folder>
```
