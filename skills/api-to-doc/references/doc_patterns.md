# API Documentation Patterns

This guide covers common patterns the skill uses to extract API information from HTML documentation.

## Pattern Recognition

### HTTP Method + Path (Most Common)

**HTML Pattern:**
```html
<code>GET /api/users</code>
<h2>GET /api/users</h2>
<li>POST /api/users/{id}</li>
```

**Regex:** `(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s<\n]+)`

**Example extraction:**
```
GET /api/users      → method: GET, path: /api/users
POST /api/users/{id} → method: POST, path: /api/users/{id}
```

### Base URL Detection

**Common locations in HTML:**

1. In meta tags or headers:
```html
<meta name="api-base-url" content="https://api.example.com">
```

2. In documentation text:
```html
<p>Base URL: <code>https://api.example.com/v1</code></p>
```

3. In JavaScript/JSON:
```html
<script>const API_BASE = "https://api.example.com"</script>
```

**Regex patterns:**
- `base\s*(?:url|uri|endpoint)[\s:]*["\']?(https?://[^\s"\'<]+)`
- `api\s*endpoint[\s:]*["\']?(https?://[^\s"\'<]+)`
- `server[\s:]*["\']?(https?://[^\s"\'<]+)`

## Common API Documentation Structures

### Swagger/OpenAPI JSON

If the API already has an OpenAPI/Swagger spec:

```json
{
  "swagger": "2.0",
  "info": { "title": "API", "version": "1.0" },
  "paths": {
    "/users": {
      "get": { "summary": "List users" }
    }
  }
}
```

**Skill behavior:** Directly extract and convert to OpenAPI 3.0.

### REST API Documentation (HTML/Markdown)

**Typical structure:**
```
## Users Endpoints

### Get all users
GET /api/users

Returns a list of all users.

### Get specific user
GET /api/users/{id}

Retrieve a single user by ID.

### Create user
POST /api/users

Create a new user.
```

**Extraction logic:**
1. Identify HTTP method + path patterns
2. Extract surrounding context as description
3. Group by resource (Users, Posts, Comments, etc.)

### Endpoint Documentation Templates

#### Pattern: Method + Path + Description

```html
<h3>Create User</h3>
<code>POST /users</code>
<p>Create a new user account.</p>
```

#### Pattern: Table Format

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | List all users |
| POST | /users | Create user |
| GET | /users/{id} | Get user by ID |

#### Pattern: List Format

```
- GET /api/posts - Retrieve all posts
- POST /api/posts - Create a new post
- GET /api/posts/{id} - Get specific post
- PUT /api/posts/{id} - Update post
- DELETE /api/posts/{id} - Delete post
```

## Path Parameter Detection

Common path parameter patterns:

- `{id}` - Resource ID
- `{userId}` - Specific resource type ID
- `:id` - Alternative syntax
- `[id]` - Alternative syntax
- `$id` - Alternative syntax

**Normalized format:** Always convert to `{paramName}` format

## Query Parameter Indicators

Look for these keywords indicating query parameters:

- `?param=value`
- `query string`
- `optional parameters`
- `filter`
- `limit`
- `offset`
- `sort`
- `search`

**Example extraction:**
```
GET /users?page=1&limit=10
Extracted: endpoint=/users, parameters=[page, limit]
```

## Request/Response Examples

When available, these can inform schema generation:

**JavaScript/JSON request example:**
```javascript
// POST /users
{
  "name": "John",
  "email": "john@example.com"
}
```

**HTML response example:**
```html
<h4>Response</h4>
<pre>
{
  "id": 1,
  "name": "John",
  "email": "john@example.com"
}
</pre>
```

## HTTP Status Codes

Common responses documented:

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid auth
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## Authentication Patterns

Look for these keywords:

- `API key`
- `Bearer token`
- `OAuth`
- `Basic auth`
- `Authorization header`
- `X-API-Key header`
- `API Key required`

**Common header patterns:**
- `Authorization: Bearer <token>`
- `Authorization: Basic <credentials>`
- `X-API-Key: <key>`
- `X-Auth-Token: <token>`

## Missing Information

When documentation is incomplete, the skill uses defaults:

- **Missing HTTP method:** Assume GET
- **Missing response type:** Assume JSON with generic object schema
- **Missing status codes:** Default to 200 for success, 400/500 for errors
- **Missing authentication:** Not included in spec (user provides via PRD)

## Example Extraction Workflow

Given this HTML:

```html
<h2>Users API</h2>
<p>Base URL: https://api.example.com/v2</p>

<h3>List Users</h3>
<code>GET /users?limit=10</code>
<p>Retrieve all users with pagination.</p>

<h3>Create User</h3>
<code>POST /users</code>
<p>Create a new user account.</p>

<h3>Get User</h3>
<code>GET /users/{id}</code>
<p>Get a specific user by ID.</p>
```

**Extracted endpoints:**
```json
{
  "title": "Users API",
  "base_url": "https://api.example.com/v2",
  "endpoints": [
    {
      "method": "GET",
      "path": "/users",
      "description": "Retrieve all users with pagination",
      "tag": "Users"
    },
    {
      "method": "POST",
      "path": "/users",
      "description": "Create a new user account",
      "tag": "Users"
    },
    {
      "method": "GET",
      "path": "/users/{id}",
      "description": "Get a specific user by ID",
      "tag": "Users"
    }
  ]
}
```
