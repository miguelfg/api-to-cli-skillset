#!/usr/bin/env python3
"""
Fetch API documentation from a URL using cURL and parse common documentation patterns.
Supports HTML documentation, Swagger/OpenAPI specs, and API reference pages.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

def fetch_url(url: str) -> str:
    """Fetch content from URL using cURL."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print(f"Error fetching {url}: {result.stderr}", file=sys.stderr)
            return ""
        return result.stdout
    except FileNotFoundError:
        print("Error: curl not found. Install curl to use this skill.", file=sys.stderr)
        sys.exit(1)

def detect_api_type(content: str, url: str) -> str:
    """Detect if content is OpenAPI, Swagger, or HTML documentation."""
    content_lower = content.lower()

    # Check for existing OpenAPI/Swagger specs
    if "openapi:" in content_lower or "swagger:" in content_lower:
        return "openapi"

    if '"openapi"' in content_lower or '"swagger"' in content_lower:
        return "swagger_json"

    # Check for common API documentation patterns
    if any(pattern in content_lower for pattern in [
        "api endpoint", "rest api", "http method",
        "request example", "response example", "authentication"
    ]):
        return "html_docs"

    # Check URL hints
    if any(pattern in url.lower() for pattern in [
        "/api/docs", "/docs", "/swagger", "/openapi",
        "/api-reference", "/api/reference"
    ]):
        return "html_docs"

    return "unknown"

def extract_endpoints_from_html(content: str) -> list:
    """Extract endpoints from HTML documentation."""
    endpoints = []

    # Pattern 1: Code blocks with HTTP methods
    http_pattern = r'(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(/[^\s<\n]+)'
    matches = re.findall(http_pattern, content)
    for method, path in matches:
        endpoints.append({
            "method": method,
            "path": path,
            "description": ""
        })

    # Pattern 2: API endpoints in headers or list items
    endpoint_pattern = r'<(?:h[2-4]|li|td)>.*?(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s<]+).*?</(?:h[2-4]|li|td)>'
    matches = re.findall(endpoint_pattern, content, re.IGNORECASE | re.DOTALL)
    for method, path in matches:
        endpoints.append({
            "method": method.upper(),
            "path": path,
            "description": ""
        })

    # Deduplicate
    seen = set()
    unique = []
    for ep in endpoints:
        key = (ep["method"], ep["path"])
        if key not in seen:
            seen.add(key)
            unique.append(ep)

    return unique

def extract_base_url(url: str, content: str) -> str:
    """Extract base URL from documentation or use the fetched URL."""
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    # Try to find API base URL in content
    patterns = [
        r'base\s*(?:url|uri|endpoint)[\s:]*["\']?(https?://[^\s"\'<]+)',
        r'api\s*endpoint[\s:]*["\']?(https?://[^\s"\'<]+)',
        r'server[\s:]*["\']?(https?://[^\s"\'<]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).rstrip("/")

    return base

def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_api_info.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = fetch_url(url)

    if not content:
        print("Failed to fetch content", file=sys.stderr)
        sys.exit(1)

    api_type = detect_api_type(content, url)

    result = {
        "url": url,
        "api_type": api_type,
        "content_length": len(content),
        "content_preview": content[:500],
    }

    if api_type == "openapi" or api_type == "swagger_json":
        result["is_spec"] = True
        try:
            result["spec"] = json.loads(content)
        except json.JSONDecodeError:
            result["spec"] = None

    elif api_type == "html_docs":
        result["is_spec"] = False
        endpoints = extract_endpoints_from_html(content)
        base_url = extract_base_url(url, content)
        result["endpoints"] = endpoints
        result["base_url"] = base_url
        result["endpoint_count"] = len(endpoints)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
