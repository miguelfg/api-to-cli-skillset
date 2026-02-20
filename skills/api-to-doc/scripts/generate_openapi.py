#!/usr/bin/env python3
"""
Generate OpenAPI 3.0.0 YAML from extracted API information or interactive input.
"""

import json
import sys
import yaml
from pathlib import Path
from datetime import datetime

def create_openapi_spec(
    title: str,
    version: str,
    base_url: str,
    endpoints: list,
    description: str = "",
    contact_name: str = "",
    contact_url: str = "",
    license_name: str = ""
) -> dict:
    """Create a basic OpenAPI 3.0.0 specification."""

    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": version,
        },
        "servers": [{"url": base_url}],
        "paths": {},
    }

    if description:
        spec["info"]["description"] = description

    if contact_name or contact_url:
        spec["info"]["contact"] = {}
        if contact_name:
            spec["info"]["contact"]["name"] = contact_name
        if contact_url:
            spec["info"]["contact"]["url"] = contact_url

    if license_name:
        spec["info"]["license"] = {"name": license_name}

    # Add endpoints
    for endpoint in endpoints:
        path = endpoint.get("path", "/")
        method = endpoint.get("method", "GET").lower()
        description = endpoint.get("description", f"{method.upper()} {path}")

        if path not in spec["paths"]:
            spec["paths"][path] = {}

        operation = {
            "summary": description,
            "tags": [endpoint.get("tag", "default")],
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            }
        }

        # Add parameters if provided
        params_data = endpoint.get("parameters", {})
        if isinstance(params_data, dict):
            # Extract path and query parameters
            path_params = params_data.get("path", []) or []
            query_params = params_data.get("query", []) or []
            body_params = params_data.get("body", []) or []

            if path_params or query_params:
                operation["parameters"] = []

                for param in path_params:
                    operation["parameters"].append({
                        "name": param.get("name", "id"),
                        "in": "path",
                        "required": True,
                        "schema": {"type": param.get("type", "string")}
                    })

                for param in query_params:
                    operation["parameters"].append({
                        "name": param.get("name", "param"),
                        "in": "query",
                        "required": param.get("required", False),
                        "schema": {"type": param.get("type", "string")}
                    })

            if body_params and method in ["post", "put", "patch"]:
                operation["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    param.get("name", f"field_{i}"): {
                                        "type": param.get("type", "string")
                                    }
                                    for i, param in enumerate(body_params)
                                },
                                "required": [p.get("name", f"field_{i}") for i, p in enumerate(body_params) if p.get("required")]
                            }
                        }
                    }
                }

        spec["paths"][path][method] = operation

    return spec

def validate_and_normalize_endpoints(endpoints: list) -> list:
    """Normalize and validate endpoint data."""
    normalized = []

    for ep in endpoints:
        normalized_ep = {
            "path": ep.get("path", "/").lstrip("/"),
            "method": ep.get("method", "GET").upper(),
            "description": ep.get("description", ""),
            "tag": ep.get("tag", "default"),
            "parameters": ep.get("parameters", {})
        }

        if not normalized_ep["path"].startswith("/"):
            normalized_ep["path"] = "/" + normalized_ep["path"]

        # Ensure valid HTTP method
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        if normalized_ep["method"] not in valid_methods:
            normalized_ep["method"] = "GET"

        normalized.append(normalized_ep)

    return normalized

def write_openapi_yaml(spec: dict, output_path: str) -> bool:
    """Write OpenAPI spec to YAML file."""
    try:
        with open(output_path, "w") as f:
            yaml.dump(spec, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error writing YAML: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_openapi.py <input_json> [output_path]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "openapi.yaml"

    try:
        with open(input_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate input
    if not data.get("endpoints"):
        print("Error: No endpoints found in input", file=sys.stderr)
        sys.exit(1)

    # Normalize endpoints
    endpoints = validate_and_normalize_endpoints(data.get("endpoints", []))

    # Create spec
    spec = create_openapi_spec(
        title=data.get("title", "API"),
        version=data.get("version", "1.0.0"),
        base_url=data.get("base_url", "http://localhost:8000"),
        endpoints=endpoints,
        description=data.get("description", ""),
        contact_name=data.get("contact_name", ""),
        contact_url=data.get("contact_url", ""),
        license_name=data.get("license_name", "")
    )

    # Write output
    if write_openapi_yaml(spec, output_path):
        print(f"✅ OpenAPI spec written to {output_path}")
        print(f"   Endpoints: {len(endpoints)}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
