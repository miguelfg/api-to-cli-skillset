# CourtListener REST API - Python Client PRD

**Version:** 2.0  
**API Version:** 4.0  
**Last Updated:** February 2025

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Authentication](#authentication)
5. [API Overview](#api-overview)
6. [Endpoint Reference](#endpoint-reference)
7. [Request Examples](#request-examples)
8. [Batch Processing](#batch-processing)
9. [Output Formats](#output-formats)
10. [Error Handling](#error-handling)
11. [Logging & Observability](#logging--observability)
12. [Rate Limiting](#rate-limiting)
13. [Performance Tips](#performance-tips)
14. [Implementation Decisions](#implementation-decisions)

---

## Introduction

### Overview

The **CourtListener REST API** provides access to federal and state case law, PACER data, the searchable RECAP Archive, oral argument recordings, judge information, and financial disclosure data. This PRD describes a Python client library and CLI tool for interacting with this comprehensive legal data API.

### Purpose

The CourtListener Python Client enables developers and researchers to:
- Search and retrieve case law and opinions
- Access PACER docket and document data
- Browse oral argument recordings
- Query judge and attorney information
- Access financial disclosure records
- Perform batch operations on large datasets
- Automate legal research workflows

### Target Audience

- Legal researchers and developers
- Law firms building case management systems
- Academic institutions conducting legal analysis
- Government agencies managing legal data
- Individual developers researching legal APIs

### Key Features

- **Comprehensive Coverage**: Access to 45 API resources (opinions, dockets, audio, people, etc.)
- **Flexible Authentication**: Token-based authentication for secure API access
- **Batch Processing**: Support for bulk operations via CSV/JSON Lines input
- **Multiple Output Formats**: JSON, CSV, XLSX export options
- **Pagination Support**: Built-in handling for large result sets
- **Async Ready**: Uses httpx library for potential async/await support
- **Rich CLI**: Click-based command-line interface with subcommands per resource

---

## Installation

### System Requirements

- Python 3.8 or higher
- pip or uv package manager
- Internet connection for API access

### Installation Methods

#### Via uv (Recommended)

```bash
uv pip install courtlistener-client
```

Or using uv's project management:
```bash
uv sync
```

#### Via pip

```bash
pip install courtlistener-client
```

#### From Source

```bash
git clone https://github.com/freelawproject/courtlistener-python-client.git
cd courtlistener-python-client
uv install
```

### Verify Installation

```bash
courtlistener-cli --version
# Output: courtlistener-cli, version 2.0.0
```

### Dependencies

- **httpx**: Modern HTTP client library (primary)
- **pydantic**: Data validation and serialization
- **click**: CLI framework
- **python-dotenv**: Environment variable loading
- **openpyxl**: XLSX file writing (for output formatting)

---

## Configuration

### Environment Variables

Configuration uses a `.env` file in your project root:

```bash
# .env.example
COURTLISTENER_API_TOKEN=your_api_token_here
COURTLISTENER_BASE_URL=https://www.courtlistener.com/api/rest/v4
COURTLISTENER_TIMEOUT=30
COURTLISTENER_LOG_LEVEL=DEBUG
COURTLISTENER_OUTPUT_FORMAT=xlsx
COURTLISTENER_INCLUDE_TIMESTAMP=true
```

### Configuration Setup

1. **Create `.env` file:**

```bash
cp .env.example .env
```

2. **Get your API token** from https://www.courtlistener.com/api/
3. **Add token to `.env`:**

```bash
COURTLISTENER_API_TOKEN=your_actual_token_here
```

4. **Set log level and output format** as needed:

```bash
COURTLISTENER_LOG_LEVEL=DEBUG
COURTLISTENER_OUTPUT_FORMAT=xlsx
```

### Configuration File

The client loads configuration in this order:
1. Environment variables (`.env` file)
2. Default values in `config.py`

---

## Authentication

### API Token

All requests to the CourtListener API require authentication via an API token (Bearer token).

**Obtain Token:**
1. Create account at https://www.courtlistener.com/
2. Go to https://www.courtlistener.com/api/
3. Generate or copy your existing API token
4. Store in `.env` file: `COURTLISTENER_API_TOKEN=your_token_here`

### Authentication Methods

#### Token Authentication (Bearer)

The client automatically uses Bearer token authentication:

```python
from courtlistener import CourtListenerClient

client = CourtListenerClient(api_token="your_token_here")
# Automatically adds: Authorization: Bearer your_token_here
```

#### Environment Variable (Recommended)

```bash
export COURTLISTENER_API_TOKEN=your_token_here
courtlistener-cli opinions list
```

### Authentication Error Handling

Common authentication errors:

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Missing/invalid token | Check token in `.env` |
| `403 Forbidden` | Token lacks permissions | Verify permissions on account |
| `429 Too Many Requests` | Rate limit exceeded | Implement backoff strategy |

### Best Practices

✓ Store tokens in `.env` (never in code)  
✓ Use environment variables for sensitive data  
✓ Rotate tokens periodically  
✓ Restrict token permissions to minimum required  
✓ Use separate tokens for development/production  

---

## API Overview

### Base URL

```
https://www.courtlistener.com/api/rest/v4
```

### API Version

CourtListener API v4 (stable, recommended)

### Resources

The API now provides **45 resources** organized by legal domain:

#### Case Law Resources
- `opinions` - Court opinions and case decisions
- `clusters` - Opinion clusters (grouped opinions)
- `opinions-cited` - Citation relationships between opinions

#### Docket Resources
- `dockets` - Case dockets
- `docket-entries` - Individual docket entries
- `bankruptcy-information` - Bankruptcy case details
- `originating-court-information` - Originating court metadata
- `docket-tags` - Docket categorization tags

#### PACER/RECAP Resources
- `recap-documents` - PACER document records
- `recap` - RECAP archive metadata
- `recap-email` - RECAP email notifications
- `recap-fetch` - RECAP document retrieval
- `recap-query` - RECAP query interface

#### Court Resources
- `courts` - Court information (federal, state)

#### Audio/Oral Argument Resources
- `audio` - Oral argument recordings

#### People Resources (14 resources)
- `people` - Judge and attorney profiles
- `positions` - Judicial positions
- `educations` - Educational backgrounds
- `schools` - Educational institutions
- `political-affiliations` - Political affiliations
- `retention-events` - Judicial retention events
- `sources` - Data sources
- `aba-ratings` - ABA judge ratings
- `attorneys` - Attorney information

#### Party & Attorney Resources
- `parties` - Case parties

#### Financial Disclosure Resources (9 resources)
- `financial-disclosures` - Judge financial disclosures
- `agreements` - Financial agreements
- `debts` - Debt records
- `gifts` - Gift records
- `investments` - Investment holdings
- `non-investment-incomes` - Income records
- `spouse-incomes` - Spouse income
- `reimbursements` - Reimbursement records
- `disclosure-positions` - Disclosure positions

#### Alert Resources
- `alerts` - User alerts
- `docket-alerts` - Docket-specific alerts
- `memberships` - User memberships

#### Tag Resources
- `tag` - Opinion tags
- `tags` - All tags

#### Other Resources
- `search` - Full-text search interface
- `prayers` - Pray and Pay project data
- `visualization` - Data visualizations
- `citation-lookup` - Citation resolution tool
- `increment-event` - Event incrementing
- `fjc-integrated-database` - FJC data

### Pagination

All list endpoints support pagination:

```bash
# Default: 20 results per page
courtlistener-cli opinions list

# Custom pagination
courtlistener-cli opinions list --limit 50 --offset 100
```

### Response Format

All responses use JSON:

```json
{
  "count": 1000,
  "next": "https://www.courtlistener.com/api/rest/v4/opinions/?limit=20&offset=40",
  "previous": "https://www.courtlistener.com/api/rest/v4/opinions/?limit=20&offset=0",
  "results": [
    {
      "id": 123456,
      "url": "https://www.courtlistener.com/api/rest/v4/opinions/123456/",
      "text": "Opinion text..."
    }
  ]
}
```

---

## Endpoint Reference

### Standard CRUD Operations

Each resource supports standard operations:

| Operation | Method | Pattern | Description |
|-----------|--------|---------|-------------|
| List | `GET` | `/visualizations` | Get paginated list |
| Create | `POST` | `/visualizations` | Create new record |
| Retrieve | `GET` | `/visualizations/{id}` | Get single record |
| Update | `PUT` | `/visualizations/{id}` | Update record |
| Delete | `DELETE` | `/visualizations/{id}` | Delete record |

### Opinions (Example Resource)

#### List Opinions

```bash
courtlistener-cli opinions list [OPTIONS]
```

**Query Parameters:**
- `limit` - Results per page (default: 20)
- `offset` - Pagination offset (default: 0)

**Example:**
```bash
courtlistener-cli opinions list --limit 50
```

#### Retrieve Opinion

```bash
courtlistener-cli opinions get <opinion_id>
```

**Example:**
```bash
courtlistener-cli opinions get 123456
```

---

## Request Examples

### Using httpx Directly

```python
import httpx

# Create client
client = httpx.Client(
    headers={"Authorization": f"Bearer {token}"}
)

# Make request
response = client.get(
    "https://www.courtlistener.com/api/rest/v4/opinions/",
    params={"limit": 20}
)
data = response.json()
print(f"Found {data['count']} opinions")
```

### cURL Examples

#### List Opinions

```bash
curl -H "Authorization: Bearer your_token_here" \
  "https://www.courtlistener.com/api/rest/v4/opinions/?limit=20"
```

#### Get Single Opinion

```bash
curl -H "Authorization: Bearer your_token_here" \
  "https://www.courtlistener.com/api/rest/v4/opinions/123456/"
```

---

## Batch Processing

### CSV Input Format

Create batch file:

```csv
method,endpoint,limit
GET,/opinions/,50
GET,/courts/,20
GET,/audio/,10
```

### Processing Batch Requests

```bash
# CSV input
courtlistener-cli batch process --input-file batch.csv --format xlsx --output results/
```

### Batch Configuration

Configure in `.env`:

```bash
COURTLISTENER_BATCH_SIZE=100
COURTLISTENER_BATCH_TIMEOUT=300
COURTLISTENER_BATCH_RETRY_ATTEMPTS=3
```

---

## Output Formats

### XLSX Output (Recommended)

Excel workbook format with formatting:

```bash
courtlistener-cli opinions list --format xlsx --output opinions.xlsx
```

**Features:**
- Formatted headers
- Column auto-sizing
- Date formatting
- Freeze panes for easy navigation

### JSON Output

Default format, fully structured:

```bash
courtlistener-cli opinions list --format json > opinions.json
```

### CSV Output

Tabular format for spreadsheets:

```bash
courtlistener-cli opinions list --format csv > opinions.csv
```

---

## Error Handling

### Common Errors

| Status | Code | Cause | Solution |
|--------|------|-------|----------|
| 400 | `bad_request` | Invalid parameters | Check query parameters |
| 401 | `unauthorized` | Missing/invalid token | Verify API token |
| 403 | `permission_denied` | Insufficient permissions | Check token scope |
| 404 | `not_found` | Resource doesn't exist | Verify resource ID |
| 429 | `rate_limit` | Rate limit exceeded | Implement backoff |
| 500 | `server_error` | Server issue | Retry after delay |

### Best Practices

✓ Always catch rate limit errors and implement backoff  
✓ Log errors for debugging  
✓ Implement circuit breaker for cascading failures  
✓ Validate input before API calls  
✓ Use timeouts to prevent hanging requests  

---

## Logging & Observability

### Log Levels

Configured via `COURTLISTENER_LOG_LEVEL`:

| Level | Usage | Example Output |
|-------|-------|--------------------|
| DEBUG | Detailed debugging | Request/response details, parameters |
| INFO | Normal operation | API calls, results count |
| WARNING | Issues to investigate | Rate limits, retries |
| ERROR | Failures | Failed requests, exceptions |

### Configuration

```bash
# .env
COURTLISTENER_LOG_LEVEL=DEBUG

# Or via CLI
courtlistener-cli --log-level debug opinions list
```

---

## Rate Limiting

### API Rate Limits

CourtListener enforces rate limits per API token:

| Plan | Requests/Hour | Requests/Day |
|------|---------------|--------------|
| Free | 60 | 500 |
| Pro | 600 | 5,000 |
| Unlimited | Unlimited | Unlimited |

### Client Rate Limiting

The client manages rate limits automatically:

```python
client = CourtListenerClient(
    api_token=token,
    rate_limit_per_second=2
)
```

---

## Performance Tips

### 1. Use Pagination Efficiently

```python
# GOOD: Stream results with iterator
for opinion in client.opinions.iter(limit=50):
    process_opinion(opinion)
```

### 2. Filter at API Level

```python
# GOOD: Filter at API level
patents = client.opinions.list(search="patent", limit=1000)
```

### 3. Batch Operations

```python
# GOOD: Use batch operations
client.batch_create(items)
```

---

## Implementation Decisions

This section documents decisions made for the generated Python client.

### HTTP Library: httpx

**Decision**: Use `httpx` for HTTP requests

**Rationale**:
- Modern, actively maintained library
- Supports both sync and async operations
- Better performance than requests
- Similar API to requests (easy migration)
- Built-in connection pooling and timeout handling

### Output Format: XLSX

**Decision**: Primary output format is XLSX (Excel)

**Rationale**:
- User preference for data analysis workflows
- Better formatting than CSV for readability
- Automatic column sizing and headers
- Supports multiple sheets for complex data

**Supported Formats**:
- XLSX (recommended)
- JSON (default for API compatibility)
- CSV (basic tabular format)

### Authentication: Environment Variables

**Decision**: Store API token in `.env` file

**Rationale**:
- Secure: Tokens never committed to code
- Convenient: Single configuration file
- Standard: Matches Python ecosystem conventions
- Flexible: Support multiple environments (dev/prod)

### Batch Input: CSV

**Decision**: Primary batch input format is CSV

**Rationale**:
- User preference for batch operations
- Easy to create with spreadsheet tools
- Standard tabular format
- Support for JSON Lines as alternative

### Logging Level: DEBUG

**Decision**: Default logging level is DEBUG

**Rationale**:
- User preference for detailed troubleshooting
- Development-friendly default
- Can be easily changed via CLI or config
- Helps with API integration debugging

---

## Summary

This PRD describes a Python CLI client for the CourtListener REST API v4 with:

- **45 API Resources** (opinions, dockets, audio, people, financial-disclosures, etc.)
- **HTTP Library**: httpx
- **Output Formats**: XLSX, JSON, CSV
- **Batch Input**: CSV
- **Logging Level**: DEBUG
- **Authentication**: Bearer token via .env
- **Batch Processing**: CSV input with progress tracking
- **Error Handling**: Specific exception classes per error type
- **Rate Limiting**: Client-side with exponential backoff

Next step: Generate the full Python Click CLI project from this PRD using `/prd-to-cli`.

