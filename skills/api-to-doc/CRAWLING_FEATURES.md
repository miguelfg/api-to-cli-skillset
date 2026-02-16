# API-to-Doc: Crawling & Caching Features

## New Features Summary

The `api-to-doc` skill now includes comprehensive HTML caching and multi-page crawling capabilities.

## Feature Overview

### 1. Automatic HTML Caching

**Location:** `/tmp/api-to-doc-cache/`

Every API documentation page fetched is automatically saved with:
- Unique filename based on URL hash
- Domain and path information included
- UTF-8 encoding for all HTML content

```bash
# View cache directory
ls -lah /tmp/api-to-doc-cache/

# Example cached filename
api_example_com_v1_docs_a1b2c3d4.html
```

**Benefits:**
- ✓ Inspect fetched content for debugging
- ✓ Reuse cached pages (faster subsequent runs)
- ✓ Enable link extraction analysis
- ✓ Keep reference copies of documentation

**Disable caching if needed:**
```bash
python scripts/fetch_api_info.py <url> --no-cache
```

### 2. Link Extraction Helper

**Script:** `scripts/link_extractor.py`

Analyzes HTML to find all crawlable API documentation pages.

```bash
# Extract links from cached HTML
python scripts/link_extractor.py /tmp/api-to-doc-cache/api_example_com_*.html https://api.example.com

# Save categorized links to JSON
python scripts/link_extractor.py page.html https://api.example.com links.json
```

**Link Categories:**
- `api_docs` - Core API documentation pages
- `endpoints` - Individual endpoint documentation
- `reference` - API reference material
- `guides` - Getting started and tutorials
- `auth` - Authentication documentation
- `examples` - Code samples and demos
- `other` - Uncategorized links

**Output:** Categorized links with URLs and crawlability assessment

### 3. Multi-Page Crawler

**Script:** `scripts/crawler.py`

Traverses multiple documentation pages to discover all API endpoints.

```bash
# Crawl starting URL (up to 10 pages)
python scripts/crawler.py https://api.example.com/docs

# Crawl with custom limits
python scripts/crawler.py https://api.example.com/docs 25 3
# Arguments: start_url [max_pages] [max_depth]
```

**Crawl Process:**
1. Start at provided URL
2. Fetch page and extract endpoints
3. Find all links on the page
4. Filter to crawlable documentation
5. Queue top 5 links for next pages
6. Repeat until max_pages reached

**Output:** Complete endpoint discovery across all pages

## Usage Workflow

### Single Page Analysis

```bash
# Step 1: Fetch documentation page
python scripts/fetch_api_info.py https://api.example.com/docs

# Step 2: Check what was cached
ls /tmp/api-to-doc-cache/

# Step 3: Extract links from cached page
python scripts/link_extractor.py /tmp/api-to-doc-cache/api_example_com_docs_*.html \
  https://api.example.com links.json

# Step 4: Review categorized links
cat links.json | jq '.categorized'
```

### Multi-Page Discovery

```bash
# Crawl entire documentation
python scripts/crawler.py https://api.example.com/docs 20 2 > crawl_results.json

# See what endpoints were discovered
cat crawl_results.json | jq '.pages[].endpoints'

# Count total unique endpoints
cat crawl_results.json | jq '.total_endpoints'
```

## Return Values

### fetch_api_info.py (Enhanced)

Now includes cache information:

```json
{
  "url": "https://api.example.com/docs",
  "api_type": "html_docs",
  "content_length": 45000,
  "cache": {
    "saved": true,
    "path": "/tmp/api-to-doc-cache/api_example_com_docs_a1b2c3d4.html",
    "cache_dir": "/tmp/api-to-doc-cache"
  },
  "endpoints": [...],
  "base_url": "https://api.example.com"
}
```

### link_extractor.py (New)

Returns categorized links:

```json
{
  "base_url": "https://api.example.com",
  "total_links": 145,
  "categorized": {
    "api_docs": 8,
    "endpoints": 12,
    "reference": 6,
    "guides": 4,
    "auth": 2,
    "examples": 5,
    "other": 102
  },
  "crawlable_count": 37,
  "crawlable_links": [
    {
      "url": "https://api.example.com/docs/endpoints/users",
      "href": "/docs/endpoints/users",
      "relative": true
    }
  ]
}
```

### crawler.py (New)

Returns comprehensive crawl results:

```json
{
  "start_url": "https://api.example.com/docs",
  "base_domain": "api.example.com",
  "pages_crawled": 10,
  "total_endpoints": 42,
  "total_links_found": 450,
  "pages": [
    {
      "url": "https://api.example.com/docs",
      "endpoints": [
        {"method": "GET", "path": "/users"},
        {"method": "POST", "path": "/users"}
      ]
    }
  ]
}
```

## Script Files Added

### `scripts/link_extractor.py`
- Extracts links from HTML
- Categorizes by relevance to API documentation
- Filters crawlable pages
- JSON output format

### `scripts/crawler.py`
- Multi-page traversal
- Endpoint discovery across pages
- Link filtering and queueing
- Configurable depth and page limits

## Integration Points

These scripts integrate with existing `api-to-doc` workflow:

```
API URL
  ↓
[fetch_api_info.py] → HTML saved to /tmp ← → [link_extractor.py] identifies crawlable links
  ↓                                           ↓
OpenAPI endpoints           or         [crawler.py] discovers all endpoints across pages
  ↓
[doc-to-prd] → PRD.md
  ↓
[prd-to-cli] → Python Click CLI
```

## Performance Characteristics

### Fetch with Caching (Default)
- First run: ~2-5 seconds per page + cache save
- Cached reads: ~0.1 seconds per page

### Link Extraction
- Small page (< 100KB): ~0.5 seconds
- Large page (500KB+): ~2 seconds

### Crawling
- 5 pages: ~10-25 seconds
- 10 pages: ~20-50 seconds
- 20 pages: ~40-100 seconds

## Cache Management

### View Cache
```bash
ls -lah /tmp/api-to-doc-cache/
du -sh /tmp/api-to-doc-cache/
```

### Clear Cache
```bash
rm -rf /tmp/api-to-doc-cache/
```

### Search Cache
```bash
grep "pattern" /tmp/api-to-doc-cache/*.html
```

## Examples

### Example 1: GitHub API Documentation

```bash
# Fetch main page
python scripts/fetch_api_info.py https://docs.github.com/en/rest

# Find crawlable pages
python scripts/link_extractor.py \
  /tmp/api-to-doc-cache/docs_github_com_en_rest_*.html \
  https://docs.github.com/en/rest \
  github_links.json

# Crawl for comprehensive endpoint discovery
python scripts/crawler.py https://docs.github.com/en/rest 15 2
```

### Example 2: Stripe API Documentation

```bash
# Fetch Stripe API reference
python scripts/fetch_api_info.py https://stripe.com/docs/api

# Extract related documentation pages
python scripts/link_extractor.py \
  /tmp/api-to-doc-cache/stripe_com_docs_api_*.html \
  https://stripe.com/docs/api \
  stripe_links.json

# View categorized links
cat stripe_links.json | jq '.categorized'

# Crawl documentation for all endpoints
python scripts/crawler.py https://stripe.com/docs/api 20
```

### Example 3: Custom API

```bash
# Single page crawl
python scripts/fetch_api_info.py https://myapi.company.com/docs

# Check cached HTML
cat /tmp/api-to-doc-cache/myapi_company_com_docs_*.html | grep -E 'GET|POST|PUT'

# Extract links for further investigation
python scripts/link_extractor.py \
  /tmp/api-to-doc-cache/myapi_company_com_docs_*.html \
  https://myapi.company.com/docs \
  myapi_links.json

# Multi-page crawl
python scripts/crawler.py https://myapi.company.com/docs 10 2 > myapi_crawl.json
```

## Troubleshooting

### "No endpoints found" in crawl
- **Cause:** Endpoints might be JavaScript-rendered
- **Solution:** Use Playwright for dynamic content rendering first

### Cache permission denied
- **Cause:** No write access to `/tmp`
- **Solution:** Use `--no-cache` or set alternative directory

### Links not categorized correctly
- **Cause:** Non-standard URL patterns
- **Solution:** Review `link_extractor.py` categorization logic

### Crawler gets stuck
- **Cause:** Redirect loops or pagination
- **Solution:** Reduce `max_depth` or check for infinite redirects

## Files & Documentation

- **[crawling_guide.md](references/crawling_guide.md)** - Comprehensive crawling guide
- **[ENHANCEMENTS.md](ENHANCEMENTS.md)** - All recent enhancements

## API Integration

The new scripts work seamlessly with the existing API:

```python
from scripts.fetch_api_info import fetch_url, get_tmp_cache_dir
from scripts.link_extractor import extract_links, categorize_links
from scripts.crawler import crawl_documentation
```

## What's Next

Future enhancements:
- [ ] Cache TTL expiration (configurable)
- [ ] Parallel page fetching
- [ ] Smart deduplication across pages
- [ ] Custom cache directory configuration
- [ ] Cache compression
- [ ] Content type filtering
- [ ] Endpoint aggregation
