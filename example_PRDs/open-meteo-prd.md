# Open-Meteo API Python Client - Product Requirements Document

**API Version:** 1.0.0
**Base URL:** `https://api.open-meteo.com`
**Generated:** 2026-02-19
**Source Spec:** `example_APIs/open-meteo/openapi.yaml`

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

---

## Introduction

### Overview

This document defines requirements for a Python Click CLI client for **Open-Meteo API**. The client should expose major `/v1/*` endpoints as subcommands and support JSON/CSV/XLSX outputs plus batch execution.

### Purpose

- Provide a fast CLI interface for weather, climate, flood, and geocoding queries
- Support reproducible automation from shell scripts and scheduled jobs
- Standardize error handling, retries, logging, and output formatting

### Target Audience

- Python developers
- Data engineers
- Analysts using weather and climate data pipelines

### Key Features

- Endpoint coverage for the discovered `/v1/*` routes
- Batch mode using CSV and TXT (JSON Lines)
- Configurable output formats (`json`, `csv`, `xlsx`)
- Connection pooling, retries, and timeout defaults

---

## Installation

### Requirements

- Python 3.8+
- `pip` or `uv`

### Setup

```bash
git clone https://github.com/your-org/open-meteo-cli.git
cd open-meteo-cli
pip install -e .
```

### Verify

```bash
open-meteo --help
```

---

## Configuration

### Environment Variables

```bash
OPEN_METEO_BASE_URL=https://api.open-meteo.com
OPEN_METEO_TIMEOUT=30
OPEN_METEO_RETRY_COUNT=3
OPEN_METEO_LOG_LEVEL=INFO
OPEN_METEO_OUTPUT_FORMAT=json
```

### Config File

Store defaults in `.open_meteo_settings.json`:

```json
{
  "base_url": "https://api.open-meteo.com",
  "timeout": 30,
  "retry_count": 3,
  "cache_enabled": true,
  "cache_ttl": 3600,
  "log_level": "INFO",
  "output_format": "json"
}
```

---

## Authentication

Open-Meteo core endpoints are public and generally do not require API keys for baseline usage. The client should still support optional key/token headers for commercial plans.

---

## Endpoint Reference

### Airquality Resource

#### 1. Get Air Quality
- Method: `GET`
- Path: `/v1/air-quality`

### Archive Resource

#### 1. Get Archive Weather
- Method: `GET`
- Path: `/v1/archive`

### Bom Resource

#### 1. Get BOM Model Forecast
- Method: `GET`
- Path: `/v1/bom`

### Climate Resource

#### 1. Get Climate Data
- Method: `GET`
- Path: `/v1/climate`

### Cma Resource

#### 1. Get CMA Model Forecast
- Method: `GET`
- Path: `/v1/cma`

### Dmi Resource

#### 1. Get DMI Model Forecast
- Method: `GET`
- Path: `/v1/dmi`

### Dwdicon Resource

#### 1. Get DWD ICON Forecast
- Method: `GET`
- Path: `/v1/dwd-icon`

### Ecmwf Resource

#### 1. Get ECMWF Forecast
- Method: `GET`
- Path: `/v1/ecmwf`

### Elevation Resource

#### 1. Get Elevation Data
- Method: `GET`
- Path: `/v1/elevation`

### Ensemble Resource

#### 1. Get Ensemble Forecast
- Method: `GET`
- Path: `/v1/ensemble`

### Flood Resource

#### 1. Get Flood Forecast
- Method: `GET`
- Path: `/v1/flood`

### Forecast Resource

#### 1. Get Weather Forecast
- Method: `GET`
- Path: `/v1/forecast`

### Gem Resource

#### 1. Get GEM Forecast
- Method: `GET`
- Path: `/v1/gem`

### Gfs Resource

#### 1. Get GFS Forecast
- Method: `GET`
- Path: `/v1/gfs`

### Jma Resource

#### 1. Get JMA Forecast
- Method: `GET`
- Path: `/v1/jma`

### Knmi Resource

#### 1. Get KNMI Forecast
- Method: `GET`
- Path: `/v1/knmi`

### Marine Resource

#### 1. Get Marine Forecast
- Method: `GET`
- Path: `/v1/marine`

### Meteofrance Resource

#### 1. Get Meteo-France Forecast
- Method: `GET`
- Path: `/v1/meteofrance`

### Metno Resource

#### 1. Get MET Norway Forecast
- Method: `GET`
- Path: `/v1/metno`

### Search Resource

#### 1. Search Locations
- Method: `GET`
- Path: `/v1/search`

---

## Input/Output Examples

```bash
open-meteo forecast list --format json
open-meteo airquality list --format csv --output-file output/air_quality.csv
open-meteo batch --input-file data/requests.csv --format xlsx
```

---

## Caching

- Default cache enabled
- Cache key based on endpoint + sorted query parameters
- TTL default: 3600 seconds
- Commands: `cache list`, `cache clear`, `cache info`

---

## Rate Limiting

- Respect server throttling and `429` responses
- Retry with exponential backoff: `1s`, `2s`, `4s` (+ jitter)
- Max attempts: `3`

---

## Error Handling

- Network and timeout errors: retry
- HTTP 4xx (except `429`): do not retry
- HTTP 5xx: retry with backoff
- Surface actionable CLI messages with endpoint and status

---

## Logging

- Default level: `INFO`
- `--verbose` enables debug logs
- Optional file logging under `logs/`
- Include request duration, cache hits, and retry attempts

---

## Best Click Practices

- One command group per resource
- Prefer options over positional args
- Support `--format`, `--output-file`, `--override`, `--verbose`
- Keep help text concise and endpoint-oriented

---

## Makefile & Project Management

```makefile
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	flake8 src/

format:
	black src/

test:
	pytest tests/ -v
```

