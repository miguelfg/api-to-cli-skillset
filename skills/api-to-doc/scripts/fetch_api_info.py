#!/usr/bin/env python3
"""
Fetch API documentation from a URL using cURL and parse common documentation patterns.
Supports HTML documentation, Swagger/OpenAPI specs, and API reference pages.
Fail-fast: if documentation cannot be reliably retrieved/extracted, exit non-zero.
"""

import json
import re
import subprocess
import sys
import hashlib
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qsl
from html.parser import HTMLParser
from html import unescape
from typing import Optional, Dict, List, Any
from datetime import datetime

from html_processing import html_to_markdown, truncate_lines

def get_tmp_cache_dir() -> Path:
    """Get or create the /tmp cache directory for API documentation."""
    cache_dir = Path("/tmp/api-to-doc-cache")
    cache_dir.mkdir(exist_ok=True, parents=True)
    return cache_dir


def get_html_cache_path(url: str) -> Path:
    """Generate a unique cache file path for a URL."""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    parsed = urlparse(url)
    domain = parsed.netloc.replace('.', '_')
    path_part = parsed.path.replace('/', '_')[:30]
    filename = f"{domain}_{path_part}_{url_hash}.html"
    return get_tmp_cache_dir() / filename


def save_html_page(url: str, content: str) -> Optional[Path]:
    """Save HTML page to /tmp cache directory."""
    try:
        cache_path = get_html_cache_path(url)
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return cache_path
    except Exception as e:
        print(f"Warning: Could not save HTML to cache: {e}", file=sys.stderr)
        return None


def fetch_url(url: str, use_cache: bool = True) -> tuple:
    """Fetch content from URL using cURL.

    Returns: (content, cache_path)
    """
    # Check cache first if enabled
    if use_cache:
        cache_path = get_html_cache_path(url)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return f.read(), cache_path
            except Exception:
                pass

    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout:
            # Save to cache
            cache_path = save_html_page(url, result.stdout)
            return result.stdout, cache_path
        # If cURL fails or returns empty, fail-fast upstream.
        print(f"⚠️  cURL returned limited results for {url}.", file=sys.stderr)
        return result.stdout if result.stdout else "", None
    except FileNotFoundError:
        print("⚠️  curl not found.", file=sys.stderr)
        return "", None

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

class HTMLContentExtractor(HTMLParser):
    """Parse HTML to extract text, code blocks, and structure."""
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.code_blocks = []
        self.current_code = ""
        self.in_code = False
        self.in_pre = False
        self.headers = []

    def handle_starttag(self, tag, attrs):
        if tag in ['code', 'pre']:
            self.in_code = True
            if tag == 'pre':
                self.in_pre = True
        elif tag == 'h1':
            self.headers.append(('h1', ''))
        elif tag in ['h2', 'h3', 'h4', 'h5']:
            self.headers.append((tag, ''))

    def handle_endtag(self, tag):
        if tag in ['code', 'pre']:
            self.in_code = False
            if self.current_code.strip():
                self.code_blocks.append(self.current_code.strip())
                self.current_code = ""
            if tag == 'pre':
                self.in_pre = False

    def handle_data(self, data):
        if self.in_code:
            self.current_code += data
        else:
            self.text_content.append(data)

def extract_endpoints_from_html(content: str) -> list:
    """Extract endpoints from HTML documentation with improved patterns."""
    endpoints = []

    # Pattern 1: Code blocks with HTTP methods (most reliable)
    http_pattern = r'(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(/[^\s<\n]+)'
    matches = re.findall(http_pattern, content)
    for method, path in matches:
        endpoints.append({
            "method": method,
            "path": path,
            "description": "",
            "parameters": [],
            "request_examples": [],
            "response_examples": []
        })

    # Pattern 2: API endpoints in headers or list items
    endpoint_pattern = r'<(?:h[2-4]|li|td)>.*?(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s<]+).*?</(?:h[2-4]|li|td)>'
    matches = re.findall(endpoint_pattern, content, re.IGNORECASE | re.DOTALL)
    for method, path in matches:
        endpoints.append({
            "method": method.upper(),
            "path": path,
            "description": "",
            "parameters": [],
            "request_examples": [],
            "response_examples": []
        })

    # Pattern 3: Explicit endpoint declarations without method.
    # Example: "The API endpoint /v1/forecast accepts ..."
    endpoint_only_pattern = r'api\s+endpoint[^<\n]*?(/v\d+/[a-zA-Z0-9_/\-]+)'
    for path in re.findall(endpoint_only_pattern, content, re.IGNORECASE):
        endpoints.append({
            "method": "GET",
            "path": path,
            "description": "",
            "parameters": [],
            "request_examples": [],
            "response_examples": []
        })

    # Pattern 3b: Endpoint wrapped in markup (e.g., "<mark>/v1/flood</mark>").
    endpoint_mark_pattern = r'api\s+endpoint.*?<mark>\s*(/v\d+/[a-zA-Z0-9_/\-]+)\s*</mark>'
    for path in re.findall(endpoint_mark_pattern, content, re.IGNORECASE | re.DOTALL):
        endpoints.append({
            "method": "GET",
            "path": path,
            "description": "",
            "parameters": [],
            "request_examples": [],
            "response_examples": []
        })

    # Pattern 4: Absolute API URLs in forms/links.
    absolute_api_pattern = r'https?://api[.\-][^"\'<>\s]+(/v\d+/[a-zA-Z0-9_/\-]+)'
    for path in re.findall(absolute_api_pattern, content, re.IGNORECASE):
        endpoints.append({
            "method": "GET",
            "path": path,
            "description": "",
            "parameters": [],
            "request_examples": [],
            "response_examples": []
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

def extract_parameters_for_endpoint(content: str, endpoint_path: str) -> Dict[str, List[Dict]]:
    """Extract query, path, and body parameters for a specific endpoint."""
    params = {
        "path": [],
        "query": [],
        "body": []
    }

    def _query_param_exists(name: str) -> bool:
        return any(p["name"] == name for p in params["query"])

    def _add_query_param(name: str, param_type: str = "string", required: bool = False):
        if not name or _query_param_exists(name):
            return
        params["query"].append({
            "name": name,
            "type": param_type,
            "required": required,
        })

    def _infer_type(type_text: str) -> str:
        t = (type_text or "").strip().lower()
        if any(k in t for k in ["int", "integer"]):
            return "integer"
        if any(k in t for k in ["float", "double", "decimal", "number"]):
            return "number"
        if "bool" in t:
            return "boolean"
        if "array" in t or "list" in t:
            return "array"
        if "object" in t or "json" in t:
            return "object"
        return "string"

    # Extract path parameters (e.g., {id}, :id, [id])
    path_param_pattern = r'[{:\[]([a-zA-Z_][a-zA-Z0-9_]*)[}\]:]'
    path_params = re.findall(path_param_pattern, endpoint_path)
    for param in path_params:
        params["path"].append({
            "name": param,
            "type": "string",
            "required": True
        })

    # Look for parameter documentation patterns near the endpoint
    context_pattern = r'(?:' + re.escape(endpoint_path) + r'|' + endpoint_path.split('/')[1] + r').*?(?=(?:GET|POST|PUT|DELETE|PATCH|####|###|##|$))'
    context = re.search(context_pattern, content, re.IGNORECASE | re.DOTALL)

    if context:
        context_text = context.group(0)

        # Query parameters
        query_pattern = r'(?:Query\s+Parameters|Query\s+String|Optional\s+Parameters|Parameters)[\s:]*\n(.*?)(?=(?:Request|Response|Request Body|Status|####|###|##|$))'
        query_match = re.search(query_pattern, context_text, re.IGNORECASE | re.DOTALL)
        if query_match:
            query_text = query_match.group(1)
            # Find parameter names in the context
            param_names = re.findall(r'(?:param|parameter|query|option)[\s:]*["\']?([a-zA-Z_][a-zA-Z0-9_]*)', query_text, re.IGNORECASE)
            for name in param_names:
                if name not in [p["name"] for p in params["query"]]:
                    _add_query_param(name, "string", False)

        # Request body parameters
        body_pattern = r'(?:Request\s+Body|Body\s+Parameters|Body|Payload)[\s:]*\n(.*?)(?=(?:Response|Status|####|###|##|$))'
        body_match = re.search(body_pattern, context_text, re.IGNORECASE | re.DOTALL)
        if body_match:
            body_text = body_match.group(1)
            param_names = re.findall(r'["\']?([a-zA-Z_][a-zA-Z0-9_]*)["\']?\s*(?::|=)', body_text)
            for name in param_names:
                if name not in [p["name"] for p in params["body"]]:
                    params["body"].append({
                        "name": name,
                        "type": "string",
                        "required": False
                    })

        # Parse concrete API URL examples and query strings in endpoint context.
        decoded_context = unescape(context_text)
        absolute_url_pattern = r'https?://api[.\-][^"\'<>\s]+'
        for full_url in re.findall(absolute_url_pattern, decoded_context, re.IGNORECASE):
            try:
                parsed_url = urlparse(full_url)
                if parsed_url.path != endpoint_path:
                    continue
                for key, _ in parse_qsl(parsed_url.query, keep_blank_values=True):
                    _add_query_param(key, "string", False)
            except Exception:
                pass

        # Handle inline URL fragments like &hourly=temperature_2m in docs text.
        for key in re.findall(r'(?:\?|&)([a-zA-Z_][a-zA-Z0-9_\-]*)=', decoded_context):
            _add_query_param(key, "string", False)

    # Parse common API docs parameter tables:
    # <tr><th>param</th><td>String array</td><td>No</td>...</tr>
    table_row_pattern = (
        r'<tr[^>]*>\s*<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>'
    )
    for raw_name, raw_type, raw_required in re.findall(table_row_pattern, content, re.IGNORECASE | re.DOTALL):
        name = re.sub(r"<[^>]+>", " ", unescape(raw_name)).strip().lower()
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_\-]*$", name):
            continue
        type_text = re.sub(r"<[^>]+>", " ", unescape(raw_type)).strip()
        req_text = re.sub(r"<[^>]+>", " ", unescape(raw_required)).strip().lower()
        required = req_text in {"yes", "required", "true"}
        _add_query_param(name, _infer_type(type_text), required)

    # Parse forms that submit directly to this endpoint and capture named inputs/selects.
    endpoint_form_pattern = (
        r'<form[^>]*action=["\']https?://[^"\']*'
        + re.escape(endpoint_path)
        + r'[^"\']*["\'][^>]*>(.*?)</form>'
    )
    for form_block in re.findall(endpoint_form_pattern, content, re.IGNORECASE | re.DOTALL):
        for name in re.findall(r'\bname=["\']([a-zA-Z_][a-zA-Z0-9_\-]*)["\']', form_block):
            _add_query_param(name, "string", False)

    return params

def extract_examples_from_content(content: str, endpoint_path: str) -> Dict[str, List[str]]:
    """Extract request and response examples for an endpoint."""
    examples = {
        "request": [],
        "response": []
    }

    # Find context around the endpoint
    context_pattern = r'(?:' + re.escape(endpoint_path) + r').*?(?=(?:GET|POST|PUT|DELETE|PATCH|###|##|$))'
    context = re.search(context_pattern, content, re.IGNORECASE | re.DOTALL)

    if not context:
        return examples

    context_text = context.group(0)

    # Extract request examples (JSON code blocks)
    request_pattern = r'(?:Request\s+Example|Example\s+Request|Request)[\s:]*\n```(?:json|javascript|js)?\s*(.*?)```'
    request_matches = re.findall(request_pattern, context_text, re.IGNORECASE | re.DOTALL)
    examples["request"].extend(request_matches)

    # Extract response examples
    response_pattern = r'(?:Response\s+Example|Example\s+Response|Response)[\s:]*\n```(?:json|javascript|js)?\s*(.*?)```'
    response_matches = re.findall(response_pattern, context_text, re.IGNORECASE | re.DOTALL)
    examples["response"].extend(response_matches)

    # Fallback: extract JSON objects from <pre> or <code> tags
    if not examples["request"] or not examples["response"]:
        json_pattern = r'(?:<pre>|<code>)(.*?)(?:</pre>|</code>)'
        json_blocks = re.findall(json_pattern, context_text, re.DOTALL)
        for block in json_blocks:
            if '{' in block:
                # Try to parse as JSON
                try:
                    json.loads(block)
                    if "request" in context_text[:context_text.find(block)].lower():
                        examples["request"].append(block.strip())
                    else:
                        examples["response"].append(block.strip())
                except:
                    pass

    return examples

def extract_base_url(url: str, content: str) -> str:
    """Extract base URL from documentation or use the fetched URL."""
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    # Prefer explicit API hosts when present in docs.
    # Supports hosts like:
    # - https://api.open-meteo.com/v1/forecast
    # - https://flood-api.open-meteo.com/v1/flood
    api_url_match = re.search(
        r'(https?://[a-zA-Z0-9.\-]*api[a-zA-Z0-9.\-]*)(?:/v\d+/[a-zA-Z0-9_/\-]*)?',
        content,
        re.IGNORECASE
    )
    if api_url_match:
        return api_url_match.group(1).rstrip("/")

    # Try to find API base URL in content
    patterns = [
        r'base\s*(?:url|uri|endpoint)[\s:]*["\']?(https?://[^\s"\'<]+)',
        r'api\s*endpoint[\s:]*["\']?(https?://[^\s"\'<]+)',
        r'server[\s:]*["\']?(https?://[^\s"\'<]+)',
        r'https?://[^\s"\'<]+/api(?:/v\d+)?'
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            url_match = match.group(0) if pattern.startswith('https') else match.group(1)
            return url_match.rstrip("/")

    return base

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch API docs and extract endpoint information."
    )
    parser.add_argument("url", help="API docs URL")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable HTML caching and force fresh download",
    )
    parser.add_argument(
        "--prefer-md-extraction",
        action="store_true",
        help="Use HTML->Markdown normalized text to extract endpoints/metadata",
    )
    parser.add_argument(
        "--save-md-cache",
        action="store_true",
        help="Save a markdown companion file next to cached HTML",
    )
    parser.add_argument(
        "--md-max-lines",
        type=int,
        default=0,
        help="Truncate generated markdown cache to N lines (0 = no truncation)",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    url = args.url
    use_cache = not args.no_cache

    content, cache_path = fetch_url(url, use_cache=use_cache)

    if not content:
        print("Failed to fetch content", file=sys.stderr)
        sys.exit(1)

    normalized_markdown = html_to_markdown(content)
    if args.md_max_lines > 0:
        normalized_markdown = truncate_lines(normalized_markdown, args.md_max_lines)

    markdown_cache_path = None
    if args.save_md_cache and cache_path:
        markdown_cache_path = cache_path.with_suffix(".md")
        markdown_cache_path.write_text(normalized_markdown, encoding="utf-8")

    api_type = detect_api_type(content, url)

    result = {
        "url": url,
        "api_type": api_type,
        "content_length": len(content),
        "content_preview": content[:500],
        "cache": {
            "saved": cache_path is not None,
            "path": str(cache_path) if cache_path else None,
            "markdown_path": str(markdown_cache_path) if markdown_cache_path else None,
            "cache_dir": str(get_tmp_cache_dir())
        }
    }

    if api_type == "openapi" or api_type == "swagger_json":
        result["is_spec"] = True
        try:
            result["spec"] = json.loads(content)
        except json.JSONDecodeError:
            result["spec"] = None

    elif api_type == "html_docs":
        result["is_spec"] = False
        extraction_source = normalized_markdown if args.prefer_md_extraction else content
        endpoints = extract_endpoints_from_html(extraction_source)
        base_url = extract_base_url(url, extraction_source)

        # Strict quality gate: no endpoint extraction means retrieval was not usable.
        if not endpoints:
            print(
                "Failed to extract real API endpoints from documentation. "
                "Failing instead of generating speculative output.",
                file=sys.stderr,
            )
            sys.exit(1)

        # Extract detailed information for each endpoint
        for endpoint in endpoints:
            endpoint["parameters"] = extract_parameters_for_endpoint(extraction_source, endpoint["path"])
            endpoint["examples"] = extract_examples_from_content(extraction_source, endpoint["path"])

        result["endpoints"] = endpoints
        result["base_url"] = base_url
        result["endpoint_count"] = len(endpoints)
        result["extraction_notes"] = [
            "Parameters extracted from documentation patterns",
            "Request/response examples sourced from code blocks",
            "HTML page saved to cache for link extraction",
            "Optional HTML-to-Markdown preprocessing available for long pages",
            "Fail-fast enabled when endpoint extraction is empty"
        ]
    else:
        print(
            "Unable to determine API documentation type from fetched content. "
            "Failing instead of generating speculative output.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
