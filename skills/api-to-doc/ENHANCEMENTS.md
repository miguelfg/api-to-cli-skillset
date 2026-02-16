# API-to-Doc Skill Enhancements

## Overview

The `api-to-doc` skill has been significantly enhanced to provide more comprehensive API documentation extraction and OpenAPI specification generation. These improvements focus on:

1. **Enhanced HTML Parsing** - Better extraction of parameters and examples
2. **Comprehensive Parameter Documentation** - Path, query, and body parameters
3. **Request/Response Example Extraction** - Automatic example parsing from code blocks
4. **Fallback Mechanisms** - Recommendations for Playwright/WebFetch when cURL is insufficient
5. **Better Documentation Pattern Recognition** - Improved patterns for identifying sections

## Key Enhancements

### 1. HTML Content Extraction (New)

**File:** `scripts/fetch_api_info.py`

Added `HTMLContentExtractor` class for parsing HTML documentation:
- Extracts text content separately from code blocks
- Identifies section headers (h1-h5)
- Preserves code block structure for pattern matching
- Handles nested HTML elements

```python
class HTMLContentExtractor(HTMLParser):
    """Parse HTML to extract text, code blocks, and structure."""
```

### 2. Enhanced Parameter Extraction (New)

**Function:** `extract_parameters_for_endpoint(content: str, endpoint_path: str) -> Dict[str, List[Dict]]`

Extracts three types of parameters:

#### Path Parameters
- Pattern: `{id}`, `:id`, `[id]`, `$id`
- Automatically extracted from endpoint paths
- Marked as required

Example:
```
GET /users/{userId}/posts/{postId}
→ Extracts: userId, postId as path parameters
```

#### Query Parameters
- Looks for sections: "Query Parameters", "Query String", "Optional Parameters"
- Extracts parameter names and infers types
- Marked as optional by default

Example:
```
Query Parameters:
  page - Page number (optional)
  limit - Results per page (optional)
→ Extracts: page, limit as query parameters
```

#### Request Body Parameters
- Looks for sections: "Request Body", "Body Parameters", "Payload"
- Extracts field names from documentation
- Inferred from JSON examples if documentation is minimal

Example:
```
Request Body:
  name (required) - User name
  email (required) - User email
→ Extracts: name, email as required body parameters
```

### 3. Request/Response Example Extraction (New)

**Function:** `extract_examples_from_content(content: str, endpoint_path: str) -> Dict[str, List[str]]`

Extracts and validates examples:
- Markdown code blocks: ````json ... ````
- HTML code blocks: `<code>...</code>`, `<pre>...</pre>`
- Searches for patterns: "Request Example", "Response Example", "Example"
- Validates JSON before including
- Returns structured examples for OpenAPI schema generation

Example:
```markdown
### Create User

POST /api/users

**Request Example:**
`​`​`json
{
  "name": "John Doe",
  "email": "john@example.com"
}
`​`​`

**Response Example:**
`​`​`json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
`​`​`
```

Extracted:
- Request: `name`, `email` fields
- Response: `id`, `name`, `email`, `created_at` fields

### 4. Enhanced OpenAPI Generation

**File:** `scripts/generate_openapi.py`

Updated `create_openapi_spec()` to include extracted parameters:

```yaml
paths:
  /users/{id}:
    get:
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
        - name: page
          in: query
          required: false
          schema:
            type: string
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name: { type: string }
                email: { type: string }
```

### 5. Fallback Mechanisms (Enhanced)

**File:** `scripts/fetch_api_info.py`

Improved `fetch_url()` to detect when cURL is insufficient:

```python
def fetch_url(url: str) -> str:
    """Fetch content from URL using cURL, with fallback mechanisms."""
    # Try cURL first
    # If returns empty or insufficient results:
    # → Print recommendation for Playwright or WebFetch
    # → Suggest browser-based extraction
```

Output example:
```
⚠️  cURL returned limited results for {url}.
Consider using browser-based extraction with Playwright or WebFetch.
```

The skill now provides structured recommendations in the JSON output:
```json
{
  "extraction_notes": [
    "Parameters extracted from documentation patterns",
    "Request/response examples sourced from code blocks",
    "Consider enhancing with browser-based extraction if incomplete"
  ]
}
```

### 6. Documentation Pattern Enhancements

**File:** `references/doc_patterns.md`

Added comprehensive patterns for:

#### Query Parameters
- "Query Parameters" section headers
- Table format specifications
- Inline patterns

#### Request Body
- "Request Body" section headers
- "Payload" documentation patterns
- Field requirement indicators

#### Path Parameters
- Format normalization (convert `:id`, `[id]` to `{id}`)
- Extraction from endpoint URLs

#### Request/Response Examples
- Markdown code block patterns
- HTML pre/code block patterns
- Labeled code example patterns
- Type inference from examples

## Data Structure Changes

### Endpoint Object (Enhanced)

Previously:
```python
{
    "method": "GET",
    "path": "/users",
    "description": ""
}
```

Now:
```python
{
    "method": "GET",
    "path": "/users/{id}",
    "description": "Get user by ID",
    "parameters": {
        "path": [
            {"name": "id", "type": "string", "required": True}
        ],
        "query": [
            {"name": "include", "type": "string", "required": False}
        ],
        "body": []
    },
    "examples": {
        "request": ["{ \"include\": \"profile\" }"],
        "response": ["{ \"id\": 1, \"name\": \"John\" }"]
    }
}
```

### Main Result Object (Enhanced)

```json
{
    "url": "https://api.example.com/docs",
    "api_type": "html_docs",
    "content_length": 45000,
    "endpoints": [...],
    "base_url": "https://api.example.com",
    "endpoint_count": 15,
    "extraction_notes": [
        "Parameters extracted from documentation patterns",
        "Request/response examples sourced from code blocks",
        "Consider enhancing with browser-based extraction if incomplete"
    ]
}
```

## Usage Examples

### Example 1: Enhanced Parameter Extraction

Input documentation:
```html
<h3>Get User</h3>
<code>GET /api/users/{userId}</code>

<h4>Path Parameters</h4>
<ul>
  <li><code>userId</code> - The user ID (required)</li>
</ul>

<h4>Query Parameters</h4>
<ul>
  <li><code>include</code> - Fields to include (optional)</li>
</ul>
```

Output (in OpenAPI):
```yaml
paths:
  /api/users/{userId}:
    get:
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
        - name: include
          in: query
          required: false
          schema:
            type: string
```

### Example 2: Request/Response Example Parsing

Input:
```markdown
### Create User

POST /api/users

**Request Example:**
\`\`\`json
{
  "name": "Alice",
  "email": "alice@example.com",
  "role": "admin"
}
\`\`\`

**Response (201):**
\`\`\`json
{
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com",
  "role": "admin",
  "created_at": "2024-01-15T10:30:00Z"
}
\`\`\`
```

Output (in OpenAPI):
```yaml
paths:
  /api/users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name: { type: string }
                email: { type: string }
                role: { type: string }
              required: [name, email]
      responses:
        '201':
          content:
            application/json:
              schema:
                type: object
                properties:
                  id: { type: integer }
                  name: { type: string }
                  email: { type: string }
                  role: { type: string }
                  created_at: { type: string }
```

## Integration with MCP Tools

When cURL is insufficient (JavaScript-rendered docs, etc.):

1. **Playwright** (webapp-testing skill)
   - Render JavaScript-heavy documentation
   - Extract dynamic content
   - Handle interactive elements

2. **WebFetch/WebSearch**
   - Alternative content fetching
   - Handle authentication/redirects
   - Gather supplementary API information

The skill now recommends these tools when detection indicates incomplete extraction.

## Backward Compatibility

All enhancements are backward compatible:
- Existing parameter extraction still works
- Optional fields default to empty if not found
- Non-matching documentation formats fall back to minimal extraction
- Interactive mode available as before

## Testing Recommendations

Test with these API documentation patterns:

1. **GitHub API** - Comprehensive parameter documentation
2. **Stripe API** - Complex request/response examples
3. **Petstore** - Multiple parameter types
4. **Custom APIs** - Various documentation formats

## Future Improvements

Consider:
- Machine learning for parameter type inference
- Automatic response schema generation
- Authentication pattern extraction
- Rate limiting documentation parsing
- Error response documentation
