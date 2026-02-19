# Tronscan API Python Client - Product Requirements Document

**Version:** 1.0.0
**Base URL:** `https://apilist.tronscanapi.com`
**Generated:** 2026-02-19
**Source Spec:** `example_APIs/tronscan-api-enhanced.yaml`

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

This document describes the Product Requirements for a Python CLI client for **Tronscan API** — the TRON blockchain explorer API for querying accounts, transactions, blocks, tokens, contracts, and analytics. The client provides a command-line interface to interact with the API, supporting batch processing, caching, rate limiting, and comprehensive error handling.

### Purpose

- Enable Python developers to quickly integrate Tronscan blockchain data into applications
- Provide a user-friendly CLI tool for querying TRON blockchain data
- Support batch operations for large-scale blockchain analytics
- Implement best practices for API interactions (caching, retry logic, rate limit handling)

### Target Audience

- Python developers building TRON blockchain applications
- Data engineers processing on-chain data from Tronscan
- DevOps engineers integrating the API into data pipelines
- Blockchain analysts querying account, block, and contract data

### Key Features

- ✓ Complete endpoint coverage: Accounts (3), Blocks (2), Contracts (3)
- ✓ XLSX output format for spreadsheet analysis
- ✓ Batch processing support (CSV/JSONL input)
- ✓ Built-in caching to reduce API calls
- ✓ Automatic retry logic with exponential backoff
- ✓ Rate limiting respects API quota
- ✓ Comprehensive logging for debugging
- ✓ Configuration management via CLI and `.env` file

---

## Installation

### System Requirements

- Python 3.8+
- uv (Python package and project manager)
- curl (optional, for manual API testing)

### Installation Methods

#### From Source

```bash
git clone https://github.com/your-org/tronscan-cli.git
cd tronscan-cli
uv sync
```

#### From PyPI

```bash
pip install tronscan-cli
```

### Verify Installation

```bash
tronscan --version
tronscan --help
```

### Dependencies

```toml
[project]
name = "tronscan-cli"
version = "1.0.0"
description = "Python CLI client for Tronscan TRON blockchain explorer API"
requires-python = ">=3.8"
dependencies = [
    "click>=8.1.0",
    "httpx>=0.27.0",
    "pandas>=1.5.0",
    "openpyxl>=3.1.0",
    "python-dotenv>=0.21.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "pylint>=2.17",
    "isort>=5.0",
]

[project.scripts]
tronscan = "tronscan_cli.cli:main"
```

---

## Configuration

### Environment Variables

Configure the client using a `.env` file or environment variables:

```bash
# Required
TRONSCAN_API_KEY=your-tron-pro-api-key-here

# Optional
TRONSCAN_BASE_URL=https://apilist.tronscanapi.com
TRONSCAN_TIMEOUT=30
TRONSCAN_VERBOSE=false
TRONSCAN_CACHE_DIR=./cache
TRONSCAN_LOG_LEVEL=INFO
TRONSCAN_OUTPUT_FORMAT=xlsx
```

### Configuration File

Configuration is stored in `.tronscan_settings.json`:

```json
{
  "api_key": "your-tron-pro-api-key",
  "base_url": "https://apilist.tronscanapi.com",
  "timeout": 30,
  "cache_enabled": true,
  "cache_ttl": 3600,
  "log_level": "INFO",
  "output_format": "xlsx",
  "verbose": false
}
```

### Configuration Management Commands

```bash
# Show current configuration
tronscan config show

# Set a configuration value
tronscan config set api_key your-new-key

# Reset to defaults
tronscan config reset

# Show cache directory
tronscan config show --include-cache
```

### Priority Order

1. CLI flags (highest priority)
2. Environment variables
3. Configuration file (`.tronscan_settings.json`)
4. Default values (lowest priority)

---

## Authentication

### API Key Authentication

The Tronscan API uses an API key passed in the `TRON-PRO-API-KEY` request header.

```bash
# Via environment variable (recommended)
export TRONSCAN_API_KEY=your-tron-pro-api-key-here

# Via CLI configuration
tronscan config set api_key your-tron-pro-api-key-here

# Via command flag (temporary override)
tronscan accounts list --api-key your-tron-pro-api-key-here
```

### Authentication Methods

**Method 1: Environment Variable (Recommended)**

```bash
export TRONSCAN_API_KEY="your-tron-pro-api-key"
tronscan accounts list
```

**Method 2: .env File**

Create a `.env` file in your project root:
```env
TRONSCAN_API_KEY=your-tron-pro-api-key
```

**Method 3: CLI Flag (Temporary)**

```bash
tronscan accounts list --api-key your-tron-pro-api-key
```

### httpx Client Setup

The client uses `httpx` with the API key header injected on every request:

```python
import httpx

client = httpx.Client(
    base_url="https://apilist.tronscanapi.com",
    headers={"TRON-PRO-API-KEY": api_key},
    timeout=30.0,
)
```

For connection pooling and session reuse, use `httpx.Client` as a context manager:

```python
with httpx.Client(base_url=BASE_URL, headers=auth_headers) as client:
    response = client.get("/api/accountv2", params={"address": address})
```

### Error Handling

- **Missing API Key:** Error message with setup instructions shown
- **Invalid API Key:** HTTP 401 response, check key validity
- **Rate Limited:** HTTP 429, automatic retry with backoff

### Best Practices

✓ Never hardcode API keys in scripts
✓ Use `.env` file and add it to `.gitignore`
✓ Rotate keys regularly
✓ Keep keys out of version control

---

## Endpoint Reference

### Resource Naming

Each API resource corresponds to a Click command group:

| Resource | Command Group | Description |
|----------|--------------|-------------|
| Accounts | `tronscan accounts` | TRON account operations |
| Blocks | `tronscan blocks` | Blockchain block data |
| Contracts | `tronscan contracts` | Smart contract info |

---

### ACCOUNTS

#### 1. List Accounts

- **Command:** `tronscan accounts list`
- **Method:** GET
- **Path:** `/api/account/list`
- **Description:** Returns a paginated list of TRON accounts, sortable by balance or other criteria.
- **Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--start` | integer | No | 0 | Start index for pagination |
| `--limit` | integer | No | 10 | Number of items per page |
| `--sort` | string | No | — | Sort criteria (e.g., `-balance` for descending balance) |

- **Response:**
  ```json
  {
    "data": [...],
    "total": 1000,
    "rangeTotal": 1000
  }
  ```
- **CLI Example:**
  ```bash
  # List top 20 accounts by balance
  tronscan accounts list --limit 20 --sort -balance

  # Paginate
  tronscan accounts list --start 100 --limit 50

  # Save to XLSX
  tronscan accounts list --limit 100 --format xlsx --output-file accounts.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/account/list", params={
      "start": 0,
      "limit": 10,
      "sort": "-balance"
  })
  ```

---

#### 2. Get Account Details

- **Command:** `tronscan accounts get`
- **Method:** GET
- **Path:** `/api/accountv2`
- **Description:** Retrieves comprehensive account information including permissions, token holdings, and staking resources.
- **Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--address` | string | **Yes** | — | TRON account address (base58 or hex) |

- **Response:**
  ```json
  {
    "address": "TAddr...",
    "balance": 1000000,
    "assetV2": {},
    "accountPermission": []
  }
  ```
- **CLI Example:**
  ```bash
  tronscan accounts get --address TAddr1234567890abcdef
  tronscan accounts get --address TAddr1234567890abcdef --format xlsx --output-file account.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/accountv2", params={"address": "TAddr..."})
  ```

---

#### 3. Get Account Tokens

- **Command:** `tronscan accounts tokens`
- **Method:** GET
- **Path:** `/api/account/tokens`
- **Description:** Lists all tokens held by an account with non-zero balance.
- **Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--address` | string | **Yes** | — | TRON account address |
| `--start` | integer | No | 0 | Start index for pagination |
| `--limit` | integer | No | 10 | Items per page |
| `--hidden` | boolean | No | false | Include hidden tokens |
| `--sort-by` | string | No | — | Sort by field name |

- **Response:**
  ```json
  {
    "data": [...],
    "total": 25
  }
  ```
- **CLI Example:**
  ```bash
  tronscan accounts tokens --address TAddr1234567890abcdef
  tronscan accounts tokens --address TAddr1234567890abcdef --limit 50 --sort-by balance
  tronscan accounts tokens --address TAddr1234567890abcdef --format xlsx --output-file tokens.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/account/tokens", params={
      "address": "TAddr...",
      "start": 0,
      "limit": 10,
      "hidden": False,
      "sortBy": "balance"
  })
  ```

---

### BLOCKS

#### 4. Get Block Information

- **Command:** `tronscan blocks list`
- **Method:** GET
- **Path:** `/api/block`
- **Description:** Returns paginated block information, optionally filtered by producer (super representative).
- **Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--start` | integer | No | 0 | Start index for pagination |
| `--limit` | integer | No | 10 | Items per page |
| `--producer` | string | No | — | Super representative address filter |
| `--sort` | string | No | `-number` | Sort criteria (default: newest first) |
| `--start-timestamp` | integer | No | — | Filter from timestamp (Unix ms) |

- **Response:**
  ```json
  {
    "data": [...],
    "total": 50000000
  }
  ```
- **CLI Example:**
  ```bash
  # List latest 20 blocks
  tronscan blocks list --limit 20

  # Blocks by a specific SR
  tronscan blocks list --producer TAddr_SR --limit 50

  # Blocks after timestamp
  tronscan blocks list --start-timestamp 1700000000000 --limit 100

  # Save to XLSX
  tronscan blocks list --limit 100 --format xlsx --output-file blocks.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/block", params={
      "start": 0,
      "limit": 10,
      "sort": "-number"
  })
  ```

---

#### 5. Get Block Statistics

- **Command:** `tronscan blocks stats`
- **Method:** GET
- **Path:** `/api/block/statistic`
- **Description:** Returns statistical summary of blocks including burn, count, and last day pay.
- **Parameters:** None

- **Response:**
  ```json
  {
    "lastDayPay": 28000000,
    "blockCount": 50000000,
    "totalBurn": 99999999
  }
  ```
- **CLI Example:**
  ```bash
  tronscan blocks stats
  tronscan blocks stats --format xlsx --output-file block_stats.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/block/statistic")
  ```

---

### CONTRACTS

#### 6. List Contracts

- **Command:** `tronscan contracts list`
- **Method:** GET
- **Path:** `/api/contracts`
- **Description:** Returns a paginated list of smart contracts with optional search and filtering.
- **Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--search` | string | No | — | Search term for contract name/address |
| `--start` | integer | No | 0 | Start index for pagination |
| `--limit` | integer | No | 10 | Items per page |
| `--sort` | string | No | — | Sort criteria |
| `--open-source-only` | boolean | No | false | Filter to open-source contracts only |

- **Response:**
  ```json
  {
    "data": [...],
    "total": 5000
  }
  ```
- **CLI Example:**
  ```bash
  tronscan contracts list --limit 20
  tronscan contracts list --search USDT --open-source-only
  tronscan contracts list --limit 100 --format xlsx --output-file contracts.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/contracts", params={
      "search": "USDT",
      "start": 0,
      "limit": 10,
      "open-source-only": True
  })
  ```

---

#### 7. Get Contract Details

- **Command:** `tronscan contracts get`
- **Method:** GET
- **Path:** `/api/contract`
- **Description:** Retrieves comprehensive details for a specific smart contract.
- **Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--contract` | string | **Yes** | — | Contract address |

- **Response:**
  ```json
  {
    "contract_address": "TAddr...",
    "name": "MyContract",
    "code": "...",
    "constructor_parameter": "..."
  }
  ```
- **CLI Example:**
  ```bash
  tronscan contracts get --contract TAddr_contract
  tronscan contracts get --contract TAddr_contract --format xlsx --output-file contract_detail.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.get("/api/contract", params={"contract": "TAddr..."})
  ```

---

#### 8. Get Contract Event Information (Batch)

- **Command:** `tronscan contracts events`
- **Method:** POST
- **Path:** `/api/contracts/smart-contract-triggers-batch`
- **Description:** Returns a list of event logs for a contract, optionally filtered by transaction hashes.
- **Parameters (Request Body):**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--contract-address` | string | No | Contract address filter |
| `--hash` | string (multiple) | No | Transaction hash(es) to filter by |
| `--term` | string | No | Search term |
| `--limit` | integer | No | Number of events to return |

- **Response:**
  ```json
  {
    "data": [...]
  }
  ```
- **CLI Example:**
  ```bash
  tronscan contracts events --contract-address TAddr_contract --limit 50
  tronscan contracts events --contract-address TAddr_contract --term Transfer --limit 100
  tronscan contracts events --contract-address TAddr_contract --format xlsx --output-file events.xlsx
  ```
- **httpx Example:**
  ```python
  response = client.post("/api/contracts/smart-contract-triggers-batch", json={
      "contractAddress": "TAddr...",
      "hashList": [],
      "term": "Transfer",
      "limit": 50
  })
  ```

---

## Input/Output Examples

### Single Request Examples

#### List Top Accounts

**Command:**
```bash
tronscan accounts list --limit 5 --sort -balance
```

**Output (XLSX):** `accounts_list.xlsx`

| address | balance | name | ... |
|---------|---------|------|-----|
| TAddr1... | 9999999 | Foundation | ... |
| TAddr2... | 8888888 | Exchange1 | ... |

---

#### Get Block Statistics

**Command:**
```bash
tronscan blocks stats --format xlsx --output-file block_stats.xlsx
```

**Output (XLSX):** `block_stats.xlsx`

| lastDayPay | blockCount | totalBurn |
|------------|------------|-----------|
| 28000000 | 50000000 | 99999999 |

---

### Batch Processing Examples

#### Batch Account Lookups (CSV Input)

**File: `data/batch_accounts.csv`**
```csv
address
TAddr1234567890abcdef
TAddr0987654321fedcba
TAddrABCDEF1234567890
```

**Command:**
```bash
tronscan batch process --input data/batch_accounts.csv --endpoint accounts-get --format xlsx
```

**Output:** `output/batch_accounts_20260219_120000.xlsx`
- Sheet `Results`: One row per account with all fields
- Sheet `Errors`: Any failed lookups with error details
- Sheet `Summary`: Total processed, success count, error count

---

#### Batch Block Queries (JSONL Input)

**File: `data/batch_blocks.jsonl`**
```jsonl
{"producer": "TAddr_SR1", "limit": 10}
{"producer": "TAddr_SR2", "limit": 10}
{"start_timestamp": 1700000000000, "limit": 5}
```

**Command:**
```bash
tronscan batch process --input data/batch_blocks.jsonl --endpoint blocks-list --format xlsx
```

---

### Output Format

#### XLSX (Default output format)

```bash
tronscan accounts list --limit 100 --format xlsx --output-file accounts.xlsx
```

- UTF-8 encoding
- Floats formatted with 0 decimal places
- No index column
- Auto-sized columns for readability
- Opens directly in Excel/LibreOffice Calc

---

## Caching

### Overview

The client caches GET API responses to reduce quota consumption on repeated queries. POST requests (contract events batch) are not cached by default.

### Cache Configuration

```bash
# Check cache status
tronscan config show | grep cache_enabled

# Bypass cache for fresh data
tronscan accounts get --address TAddr... --override

# Disable caching permanently
tronscan config set cache_enabled false
```

**Cache Location:**

```bash
# Default: ~/.cache/tronscan/
# Custom location:
tronscan config set cache_dir /custom/cache/path
```

**Cache TTL (Time-To-Live):**

```bash
# View current TTL (default: 3600 seconds / 1 hour)
tronscan config show | grep cache_ttl

# Set custom TTL (in seconds)
tronscan config set cache_ttl 1800  # 30 minutes for faster-changing blockchain data
```

### Cache Management Commands

```bash
tronscan cache list
tronscan cache info
tronscan cache delete --key accounts_list_abc123
tronscan cache clear --confirm
```

### Cache Key Strategy

```
Method:Endpoint:ParamHash
GET:/api/accountv2:sha256(address=TAddr...)
GET:/api/block:sha256(start=0&limit=10&sort=-number)
```

### Best Practices

✓ Use caching for account/contract lookups (data changes infrequently)
✓ Set shorter TTL (300–600s) for block data (new blocks every ~3 seconds on TRON)
✓ Bypass cache (`--override`) for real-time balance checks
✓ Clear cache after long gaps between sessions

---

## Rate Limiting

### API Rate Limits

Tronscan API enforces rate limits based on the `TRON-PRO-API-KEY` tier:

- **Free tier:** ~15 requests/second
- **Pro tier:** Higher limits based on plan
- **Burst:** May vary; always handle 429 gracefully

### Client Rate Limiting

The client implements:

**Courtesy Delay:**
- 100ms delay between consecutive requests
- Prevents accidental rate limit violations

**Automatic Retry on 429:**
- Max attempts: 3
- Delays: 1s → 2s → 4s (exponential backoff)
- Jitter: ±10% randomization

### Configuration

```bash
tronscan config set max_retries 3
tronscan config set backoff_multiplier 2
tronscan config set courtesy_delay 100  # milliseconds
```

### Rate Limit Handling Example

```bash
tronscan accounts list --verbose
# [INFO] GET /api/account/list (0.23s, cached=false)
# [WARNING] Rate limited (429), retrying in 1.1 seconds...
# [INFO] Retry 1/3 successful
```

---

## Error Handling

### Error Classification

| Category | HTTP Codes | Action |
|----------|-----------|--------|
| Network | 5xx, timeout | Auto-retry with backoff |
| Rate Limit | 429 | Auto-retry with longer backoff |
| Client | 400, 401, 403, 404 | Display error, no retry |
| Data | — | Raise exception with details |

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/missing `TRON-PRO-API-KEY` | Check `TRONSCAN_API_KEY` in `.env` |
| 403 Forbidden | Insufficient API key tier | Upgrade Tronscan API plan |
| 404 Not Found | Invalid address or contract | Verify address on tronscan.org |
| 429 Too Many Requests | Rate limit exceeded | Reduce request frequency; auto-retry handles this |
| 500 Server Error | Tronscan API issue | Retry later (auto-retry enabled) |
| Connection timeout | Network issue | Check connectivity |

### Error Output

```bash
tronscan accounts get --address INVALID_ADDR 2>&1
# Error: Account not found (404) — address: INVALID_ADDR
# Tip: Verify address at https://tronscan.org/#/address/INVALID_ADDR

tronscan accounts get --address TAddr... --verbose
# [DEBUG] GET /api/accountv2?address=TAddr...
# [DEBUG] Response 200: {"address": "TAddr...", ...}
```

### Best Practices

✓ Use `--verbose` for debugging
✓ Validate TRON addresses before batch operations
✓ Check logs for retry patterns indicating rate limit issues
✗ Don't retry immediately on 4xx errors

---

## Logging

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Full request/response payloads, headers |
| INFO (default) | API calls, cache hits, timing, retries |
| WARNING | Rate limit events, deprecated endpoints |
| ERROR | Failed requests, validation errors |

### Configuration

```bash
tronscan config set log_level DEBUG
export TRONSCAN_LOG_LEVEL=DEBUG
tronscan accounts list --verbose  # equivalent to DEBUG for this request
```

### Log Format

```
2026-02-19 12:30:45,123 - tronscan - INFO - GET /api/account/list (0.42s, cached=false)
2026-02-19 12:30:45,200 - tronscan - INFO - Saved 100 rows → output/accounts.xlsx
2026-02-19 12:30:46,301 - tronscan - WARNING - 429 Rate limited, retry 1/3 in 1.1s
2026-02-19 12:30:47,512 - tronscan - INFO - GET /api/block (0.31s, cached=true) [CACHE HIT]
```

### Log File Location

```
~/.cache/tronscan/tronscan.log
```

---

## Best Click Practices

### CLI Command Design

```bash
# ✓ Good: options with --help discoverability
tronscan accounts get --address TAddr...
tronscan blocks list --limit 50 --sort -number

# ✗ Bad: positional arguments
tronscan accounts get TAddr...
```

### Standard Options (All Commands)

```
--format xlsx               Output format (xlsx)
--output-file PATH          Save output to file
--verbose                   Show detailed debug output
--api-key KEY               Override API key for this call
--timeout SECONDS           Request timeout (default: 30)
--no-cache                  Skip cache for this request
--override                  Force fresh fetch (bypass cache)
--dry-run                   Show request without executing
```

### Pagination Options (List Commands)

```
--start N                   Start index (default: 0)
--limit N                   Items per page (default: 10, max: 200)
--sort FIELD                Sort expression (e.g., -balance)
```

### Command Hierarchy

```
tronscan
├── accounts
│   ├── list              # GET /api/account/list
│   ├── get               # GET /api/accountv2
│   └── tokens            # GET /api/account/tokens
├── blocks
│   ├── list              # GET /api/block
│   └── stats             # GET /api/block/statistic
├── contracts
│   ├── list              # GET /api/contracts
│   ├── get               # GET /api/contract
│   └── events            # POST /api/contracts/smart-contract-triggers-batch
├── batch
│   └── process           # Batch processing from CSV/JSONL
├── cache
│   ├── list
│   ├── info
│   ├── delete
│   └── clear
└── config
    ├── show
    ├── set
    └── reset
```

### Error Messages

```
✓ Error: Account not found (404) — address: INVALID_ADDR
✓ Solution: Verify address at https://tronscan.org or use 'tronscan accounts list'

✗ Error: 404
```

---

## Makefile & Project Management

### Project Structure

```
tronscan-cli/
├── Makefile
├── pyproject.toml
├── uv.lock
├── README.md
├── .env.example
├── src/
│   └── tronscan_cli/
│       ├── __init__.py
│       ├── cli.py                    # Click root group
│       ├── client.py                 # httpx client wrapper
│       ├── config.py                 # .env + settings management
│       ├── cache.py                  # Cache logic
│       ├── logger.py                 # Logging setup
│       └── commands/
│           ├── __init__.py
│           ├── accounts.py           # accounts list/get/tokens
│           ├── blocks.py             # blocks list/stats
│           └── contracts.py          # contracts list/get/events
├── data/                             # User batch input files
├── output/                           # Generated XLSX output
├── tests/
│   ├── conftest.py
│   ├── test_cli.py
│   └── test_client.py
└── examples/
    ├── batch_accounts.csv
    ├── batch_blocks.jsonl
    └── basic_usage.sh
```

### .env.example

```env
# Required
TRONSCAN_API_KEY=your-tron-pro-api-key-here

# Optional
TRONSCAN_BASE_URL=https://apilist.tronscanapi.com
TRONSCAN_TIMEOUT=30
TRONSCAN_CACHE_DIR=./cache
TRONSCAN_LOG_LEVEL=INFO
TRONSCAN_OUTPUT_FORMAT=xlsx
```

### Makefile

```makefile
.PHONY: help install install-dev lint format test test-cov clean build

PROJECT_NAME := tronscan

help:
	@echo "tronscan-cli — Available commands:"
	@echo ""
	@echo "  Setup:"
	@echo "    make install          Install dependencies (uv sync)"
	@echo "    make install-dev      Install with dev dependencies"
	@echo ""
	@echo "  Development:"
	@echo "    make lint             Run linters"
	@echo "    make format           Format code"
	@echo "    make test             Run tests"
	@echo "    make test-cov         Run tests with coverage"
	@echo "    make clean            Clean artifacts"
	@echo ""
	@echo "  CLI examples:"
	@echo "    make accounts-list    List top accounts"
	@echo "    make accounts-get     Get account details (ADDRESS=...)"
	@echo "    make blocks-list      List latest blocks"
	@echo "    make blocks-stats     Get block statistics"
	@echo "    make contracts-list   List smart contracts"
	@echo "    make contracts-get    Get contract details (CONTRACT=...)"

install:
	uv sync

install-dev:
	uv sync --all-extras

lint:
	uv run black --check src/
	uv run pylint src/

format:
	uv run black src/
	uv run isort src/

test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ -v --cov=src/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	uv build

# Endpoint shortcuts
accounts-list:
	uv run $(PROJECT_NAME) accounts list --limit 20 --sort -balance

accounts-get:
	uv run $(PROJECT_NAME) accounts get --address $(ADDRESS)

blocks-list:
	uv run $(PROJECT_NAME) blocks list --limit 20

blocks-stats:
	uv run $(PROJECT_NAME) blocks stats

contracts-list:
	uv run $(PROJECT_NAME) contracts list --limit 20

contracts-get:
	uv run $(PROJECT_NAME) contracts get --contract $(CONTRACT)

.DEFAULT_GOAL := help
```

### Using uv

```bash
# Setup
uv sync

# Run CLI
uv run tronscan accounts list --limit 10
uv run tronscan blocks stats
uv run tronscan contracts list --search USDT

# Tests
uv run pytest tests/ -v

# Format
uv run black src/
uv run isort src/
```

---

## Summary

This PRD covers a production-ready Python CLI client for the **Tronscan TRON Blockchain Explorer API** with:

- **3 resources:** Accounts, Blocks, Contracts
- **8 endpoints** with full parameter documentation and httpx examples
- **httpx** for HTTP requests with connection pooling
- **XLSX** output via pandas + openpyxl
- **Batch processing** from CSV/JSONL files
- **Caching** with configurable TTL (recommended: short TTL for block data)
- **Retry logic** with exponential backoff for rate limits
- **uv** for project and dependency management

For additional help:

```bash
tronscan --help
tronscan accounts --help
tronscan blocks --help
tronscan contracts --help
```

**API Docs:** https://docs.tronscan.org/
**API Server:** https://apilist.tronscanapi.com/
**Explorer:** https://tronscan.org/
