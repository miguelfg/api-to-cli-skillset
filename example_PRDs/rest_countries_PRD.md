# REST Countries API Python Client - Product Requirements Document

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Authentication](#authentication)
5. [Endpoint Reference](#endpoint-reference)
6. [Input/Output Examples](#inputoutput-examples)
7. [Caching](#caching)
8. [Rate Limiting](#rate-limiting)
9. [Error Handling](#error-handling)
10. [Logging](#logging)
11. [Best Click Practices](#best-click-practices)
12. [Makefile & Project Management](#makefile--project-management)

## Introduction

### Overview

This PRD defines requirements for a Python Click CLI client for the REST Countries API.

**API Version:** 3.1
**Base URL:** `https://restcountries.com`
**CLI Name:** `restcountries-cli`

### Purpose

- Provide fast country lookup commands from the terminal.
- Support field filtering and exportable structured output.
- Support batch lookups for repeated workflows.

### Key Features

- Endpoint coverage for major REST Countries v3.1 lookups.
- Output formats: JSON, CSV, XLSX.
- Batch input processing.
- Configurable logging, caching, retries, and timeouts.

## Installation

### Requirements

- Python 3.10+
- pip or uv

### Install

```bash
uv sync
```

### Verify

```bash
python -m src.cli --help
```

## Configuration

Use environment variables and a local JSON settings file.

```bash
RESTCOUNTRIES_BASE_URL=https://restcountries.com
RESTCOUNTRIES_TIMEOUT=30
RESTCOUNTRIES_VERBOSE=false
RESTCOUNTRIES_CACHE_DIR=.cache/restcountries
RESTCOUNTRIES_CACHE_TTL=3600
```

Example settings file (`.restcountries_cli_settings.json`):

```json
{
  "base_url": "https://restcountries.com",
  "timeout": 30,
  "cache_enabled": true,
  "cache_ttl": 3600,
  "log_level": "INFO",
  "output_format": "json"
}
```

## Authentication

No authentication is required for REST Countries public endpoints.

## Endpoint Reference

### Countries Resource

#### 1. List All Countries
- Method: GET
- Path: `/v3.1/all`
- Description: Returns all countries.
- Query Parameters:
  - `fields` (optional, comma-separated up to 10 fields)

#### 2. List by Independence Status
- Method: GET
- Path: `/v3.1/independent`
- Description: Returns countries filtered by independence status.
- Query Parameters:
  - `status` (optional, boolean; default true)
  - `fields` (optional)

#### 3. Search by Name
- Method: GET
- Path: `/v3.1/name/{name}`
- Description: Search countries by common or official name.
- Path Parameters:
  - `name` (required)
- Query Parameters:
  - `fields` (optional)

#### 4. Search by Full Name
- Method: GET
- Path: `/v3.1/name/{name}`
- Description: Exact full name match.
- Path Parameters:
  - `name` (required)
- Query Parameters:
  - `fullText=true` (required for this mode)
  - `fields` (optional)

#### 5. Search by Code
- Method: GET
- Path: `/v3.1/alpha/{code}`
- Description: Search by cca2, ccn3, cca3, or cioc code.
- Path Parameters:
  - `code` (required)
- Query Parameters:
  - `fields` (optional)

#### 6. Search by List of Codes
- Method: GET
- Path: `/v3.1/alpha`
- Description: Search multiple countries by codes.
- Query Parameters:
  - `codes` (required, comma-separated)
  - `fields` (optional)

#### 7. Search by Currency
- Method: GET
- Path: `/v3.1/currency/{currency}`
- Description: Search by currency code or name.
- Path Parameters:
  - `currency` (required)
- Query Parameters:
  - `fields` (optional)

#### 8. Search by Demonym
- Method: GET
- Path: `/v3.1/demonym/{demonym}`
- Description: Search by demonym.
- Path Parameters:
  - `demonym` (required)
- Query Parameters:
  - `fields` (optional)

#### 9. Search by Language
- Method: GET
- Path: `/v3.1/lang/{language}`
- Description: Search by language code or name.
- Path Parameters:
  - `language` (required)
- Query Parameters:
  - `fields` (optional)

#### 10. Search by Capital
- Method: GET
- Path: `/v3.1/capital/{capital}`
- Description: Search by capital city.
- Path Parameters:
  - `capital` (required)
- Query Parameters:
  - `fields` (optional)

#### 11. Search by Region or Subregion
- Method: GET
- Path: `/v3.1/region/{region}` and `/v3.1/subregion/{subregion}`
- Description: Filter countries by region or subregion.
- Path Parameters:
  - `region` or `subregion` (required)
- Query Parameters:
  - `fields` (optional)

#### 12. Search by Translation
- Method: GET
- Path: `/v3.1/translation/{translation}`
- Description: Search countries using translated country names.
- Path Parameters:
  - `translation` (required)
- Query Parameters:
  - `fields` (optional)

## Input/Output Examples

Single query:

```bash
restcountries-cli countries by-name --name germany --fields name,capital,population --format json
```

Batch query:

```bash
restcountries-cli batch --input-file countries.csv --format csv --output-path ./output
```

## Caching

- Cache key is derived from endpoint path + query parameters.
- Default TTL: 3600 seconds.
- Add `--override` to bypass cache.
- Provide cache commands: list, clear, info, delete.

## Rate Limiting

- Add 100ms delay between requests by default.
- Retry on: 408, 429, 500, 502, 503, 504.
- Exponential backoff: 1s, 2s, 4s with jitter.

## Error Handling

- Network errors: retry with backoff.
- 4xx errors: show clear message and stop (except 429).
- Parsing errors: show endpoint and payload context.
- Return non-zero exit code for failures.

## Logging

- Levels: DEBUG, INFO, WARNING, ERROR.
- Include request path, params, status code, cache hit/miss, elapsed ms.
- `--verbose` enables DEBUG-level request diagnostics.

## Best Click Practices

- Use command groups by resource (`countries`).
- Prefer options over positional args.
- Support `--format`, `--output-file`, `--limit`, `--skip`, `--override`, `--verbose`.
- Provide actionable error messages.

## Makefile & Project Management

Suggested targets:

```makefile
install:
	uv sync

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

run-help:
	uv run python -m src.cli --help
```
