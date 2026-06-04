# Arkham Intel API - Python CLI Product Requirements Document

## Table of Contents

1. [Introduction](#introduction)
2. [Implementation Decisions](#implementation-decisions)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Authentication](#authentication)
6. [Endpoint Reference](#endpoint-reference)
7. [Input/Output Examples](#inputoutput-examples)
8. [Caching](#caching)
9. [Rate Limiting](#rate-limiting)
10. [Error Handling](#error-handling)
11. [Logging](#logging)
12. [Best Click Practices](#best-click-practices)
13. [Makefile & Project Management](#makefile--project-management)
14. [Implementation Checklist](#implementation-checklist)

---

## Introduction

### Overview

This document specifies requirements for a Python CLI client for the **Arkham Intel API** — an on-chain intelligence platform providing blockchain address/entity analysis, transfer tracking, portfolio data, and token market information.

**Source spec:** `example_APIs/arkm-intel-api-v1/openapi.yaml` (OpenAPI 3.0.0, version 1.1.0)

### Purpose

- Provide CLI access to Arkham's blockchain intelligence data
- Support batch address/entity lookups for large-scale analysis
- Enable data engineers to pull transfer, portfolio, and intelligence data into pipelines
- Cover all 82 documented endpoints across 20 resource groups

### Key Features

- ✓ Full endpoint coverage (82 endpoints, 20 resource groups)
- ✓ Batch address intelligence (up to 1000 addresses per request)
- ✓ Multiple output formats (JSON, CSV, XLSX)
- ✓ Batch input from CSV/JSONL files
- ✓ Automatic retry with exponential backoff
- ✓ Rate limiting (transfers endpoint: 1 req/sec)
- ✓ Environment-variable credential management
- ✓ WebSocket session management

---

## Implementation Decisions

- CLI Name: `arkm`
- Python Version: `>=3.10`
- HTTP Library: `requests`
- Authentication: `API-Key` request header (value from `ARKM_API_KEY` env var)
- Credentials Configuration: `env_vars`
- Timeout: `30s total timeout`
- Retry Policy: `3 attempts, 1s base, x2 backoff, retry on 408,429,500,502,503,504`
- Output Formats: `json,csv,xlsx`
- Output Accepted Formats and Default: `default_xlsx__accepted_xlsx_csv`
- Batch Input Formats: `csv + txt/jsonl`
- Default Save Data Mode: `timestamped`
- Lint/Format Toolchain: `ruff check --fix` + `ruff format`

---

## Installation

```bash
uv venv && uv pip install -e ".[dev]"
```

**Run any command:**
```bash
uv run arkm <resource> <command> [OPTIONS]
```

### Package structure

```
arkm-cli/
├── pyproject.toml
├── .env.example
├── Makefile
├── src/
│   ├── __init__.py
│   ├── cli.py           # Main Click group
│   ├── client.py        # HTTP client with auth + retry
│   ├── config.py        # Env var loading
│   ├── output.py        # JSON/CSV/XLSX formatters
│   ├── batch_processor.py
│   ├── logger.py
│   └── commands/
│       ├── __init__.py
│       ├── arkm_commands.py
│       ├── balances_commands.py
│       ├── chains_commands.py
│       ├── cluster_commands.py
│       ├── counterparties_commands.py
│       ├── flow_commands.py
│       ├── history_commands.py
│       ├── intelligence_commands.py
│       ├── loans_commands.py
│       ├── marketdata_commands.py
│       ├── networks_commands.py
│       ├── portfolio_commands.py
│       ├── swaps_commands.py
│       ├── tag_commands.py
│       ├── token_commands.py
│       ├── transfers_commands.py
│       ├── tx_commands.py
│       ├── user_commands.py
│       ├── volume_commands.py
│       └── ws_commands.py
└── tests/
    └── test_cli.py
```

---

## Configuration

**Required environment variable:**
```
ARKM_API_KEY=<your-api-key>
```

**Optional:**
```
ARKM_BASE_URL=https://api.arkm.com   # default
ARKM_TIMEOUT=30
ARKM_LOG_LEVEL=INFO
```

Load from `.env` file using `python-dotenv`. `.env` must be git-ignored.

**`.env.example`:**
```
ARKM_API_KEY=your_api_key_here
ARKM_BASE_URL=https://api.arkm.com
ARKM_TIMEOUT=30
ARKM_LOG_LEVEL=INFO
```

---

## Authentication

**Method:** HTTP request header  
**Header name:** `API-Key`  
**Value source:** `ARKM_API_KEY` environment variable  

All requests must include:
```
API-Key: <value of ARKM_API_KEY>
```

**Auth tiers noted in spec:**
- Standard API key: required for most endpoints
- API tier authentication: required for `/transfers/histogram`, `/transfers/histogram/simple` — same header, but account must have API tier subscription

If `ARKM_API_KEY` is missing, exit immediately with a clear error message before making any request.

**Base URL:** `https://api.arkm.com`  
**WebSocket URL:** `wss://api.arkm.com/ws/transfers`

---

## Endpoint Reference

**Resources:** `arkm, balances, chains, cluster, counterparties, flow, history, intelligence, loans, marketdata, networks, portfolio, swaps, tag, token, transfers, tx, user, volume, ws`

---

### ARKM Resource

#### 1. Get circulating supply
- `GET /arkm/circulating`
- No parameters
- Returns circulating ARKM token supply

---

### BALANCES Resource

#### 1. Get balances by address
- `GET /balances/address/{address}`
- Path: `address` (string, required) — blockchain address
- Query: `chains` (string) — comma-separated chain list (e.g. `ethereum,bsc`)

#### 2. Get balances by entity
- `GET /balances/entity/{entity}`
- Path: `entity` (string, required) — entity slug (e.g. `binance`)
- Query: `chains` (string)

#### 3. Get Solana subaccount balances by address
- `GET /balances/solana/subaccounts/address/{addresses}`
- Path: `addresses` (string, required) — comma-separated Solana addresses

#### 4. Get Solana subaccount balances by entity
- `GET /balances/solana/subaccounts/entity/{entities}`
- Path: `entities` (string, required) — comma-separated entity slugs

---

### CHAINS Resource

#### 1. List supported chains
- `GET /chains`
- No parameters
- Returns list of all supported blockchain networks

---

### CLUSTER Resource

#### 1. Get cluster summary
- `GET /cluster/{id}/summary`
- Path: `id` (string, required) — cluster ID

---

### COUNTERPARTIES Resource

#### 1. Get counterparties for address
- `GET /counterparties/address/{address}`
- Path: `address` (string, required)
- Query: `chains`, `flow` (`in|out|all`), `tokens`, `timeLast`, `timeGte`, `timeLte`, `usdGte`, `usdLte`, `limit`, `offset`

#### 2. Get counterparties for entity
- `GET /counterparties/entity/{entity}`
- Path: `entity` (string, required)
- Query: same as address counterparties

---

### FLOW Resource

#### 1. Get fund flow for address
- `GET /flow/address/{address}`
- Path: `address` (string, required)
- Query: `chains`, `flow`, `tokens`, `timeLast`, `timeGte`, `timeLte`, `usdGte`, `usdLte`

#### 2. Get fund flow for entity
- `GET /flow/entity/{entity}`
- Path: `entity` (string, required)
- Query: same as address flow

---

### HISTORY Resource

#### 1. Get transaction history for address
- `GET /history/address/{address}`
- Path: `address` (string, required)
- Query: `chains`, `limit`, `offset`

#### 2. Get transaction history for entity
- `GET /history/entity/{entity}`
- Path: `entity` (string, required)
- Query: `chains`, `limit`, `offset`

---

### INTELLIGENCE Resource

#### 1. Get address intelligence
- `GET /intelligence/address/{address}`
- Path: `address` (string, required)
- Query: `chain` (string) — specific chain

#### 2. Get address intelligence (all chains)
- `GET /intelligence/address/{address}/all`
- Path: `address` (string, required)

#### 3. Batch address intelligence
- `POST /intelligence/address/batch`
- Body: `{"addresses": ["0x...", ...]}`  — up to 1000 addresses
- Query: `chains` (string), `chain` (string)

#### 4. Batch address intelligence (all chains)
- `POST /intelligence/address/batch/all`
- Body: `{"addresses": ["0x...", ...]}`
- Query: `chains` (string), `chain` (string)

#### 5. Get enriched address intelligence
- `GET /intelligence/address_enriched/{address}`
- Path: `address` (string, required)
- Query: `chain` (string)

#### 6. Get enriched address intelligence (all chains)
- `GET /intelligence/address_enriched/{address}/all`
- Path: `address` (string, required)

#### 7. Batch enriched address intelligence
- `POST /intelligence/address_enriched/batch`
- Body: `{"addresses": ["0x...", ...]}`  — up to 1000 addresses

#### 8. Batch enriched address intelligence (all chains)
- `POST /intelligence/address_enriched/batch/all`
- Body: `{"addresses": ["0x...", ...]}`

#### 9. Get address tag updates
- `GET /intelligence/address_tags/updates`
- Query: `limit`, `offset`, `timeGte`, `timeLte`

#### 10. Get address updates
- `GET /intelligence/addresses/updates`
- Query: `limit`, `offset`, `timeGte`, `timeLte`

#### 11. Get contract intelligence
- `GET /intelligence/contract/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)

#### 12. Get entity updates
- `GET /intelligence/entities/updates`
- Query: `limit`, `offset`, `timeGte`, `timeLte`

#### 13. Get entity intelligence
- `GET /intelligence/entity/{entity}`
- Path: `entity` (string, required)

#### 14. Get entity summary
- `GET /intelligence/entity/{entity}/summary`
- Path: `entity` (string, required)

#### 15. Get entity balance changes
- `GET /intelligence/entity_balance_changes`
- Query: `entity`, `timeGte`, `timeLte`, `limit`, `offset`

#### 16. Get entity predictions
- `GET /intelligence/entity_predictions/{entity}`
- Path: `entity` (string, required)

#### 17. Get entity types
- `GET /intelligence/entity_types`
- No parameters

#### 18. Search intelligence
- `GET /intelligence/search`
- Query: `query` (string, required) — search term

#### 19. Get tag updates
- `GET /intelligence/tags/updates`
- Query: `limit`, `offset`, `timeGte`, `timeLte`

#### 20. Get token intelligence by chain/address
- `GET /intelligence/token/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)

#### 21. Get token intelligence by ID
- `GET /intelligence/token/{id}`
- Path: `id` (string, required) — token identifier

---

### LOANS Resource

#### 1. Get loans for address
- `GET /loans/address/{address}`
- Path: `address` (string, required)
- Query: `chains`

#### 2. Get loans for entity
- `GET /loans/entity/{entity}`
- Path: `entity` (string, required)
- Query: `chains`

---

### MARKETDATA Resource

#### 1. Get altcoin index
- `GET /marketdata/altcoin_index`
- No parameters

---

### NETWORKS Resource

#### 1. Get chain network history
- `GET /networks/history/{chain}`
- Path: `chain` (string, required) — e.g. `ethereum`
- Query: `timeGte`, `timeLte`

#### 2. Get network status
- `GET /networks/status`
- No parameters

---

### PORTFOLIO Resource

#### 1. Get portfolio for address
- `GET /portfolio/address/{address}`
- Path: `address` (string, required)
- Query: `chains`

#### 2. Get portfolio for entity
- `GET /portfolio/entity/{entity}`
- Path: `entity` (string, required)
- Query: `chains`

#### 3. Get portfolio time series for address
- `GET /portfolio/timeSeries/address/{address}`
- Path: `address` (string, required)
- Query: `chains`, `timeGte`, `timeLte`

#### 4. Get portfolio time series for entity
- `GET /portfolio/timeSeries/entity/{entity}`
- Path: `entity` (string, required)
- Query: `chains`, `timeGte`, `timeLte`

---

### SWAPS Resource

#### 1. Get swaps
- `GET /swaps`
- Query: `base`, `chains`, `flow`, `from`, `to`, `tokens`, `timeGte`, `timeLte`, `timeLast`, `usdGte`, `usdLte`, `sortKey`, `sortDir`, `limit` (default 50), `offset` (default 0)

---

### TAG Resource

#### 1. Get tag parameters
- `GET /tag/{id}/params`
- Path: `id` (string, required) — tag ID

#### 2. Get tag summary
- `GET /tag/{id}/summary`
- Path: `id` (string, required)

---

### TOKEN Resource

#### 1. Get token addresses
- `GET /token/addresses/{id}`
- Path: `id` (string, required) — token identifier

#### 2. Get Arkham exchange tokens
- `GET /token/arkham_exchange_tokens`
- No parameters

#### 3. Get token balance by chain/address
- `GET /token/balance/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)

#### 4. Get token balance by ID
- `GET /token/balance/{id}`
- Path: `id` (string, required)

#### 5. Get token holders by chain/address
- `GET /token/holders/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)

#### 6. Get token holders by ID
- `GET /token/holders/{id}`
- Path: `id` (string, required)

#### 7. Get token market data
- `GET /token/market/{id}`
- Path: `id` (string, required)

#### 8. Get token price history by chain/address
- `GET /token/price/history/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)
- Query: `timeGte`, `timeLte`

#### 9. Get token price history by ID
- `GET /token/price/history/{id}`
- Path: `id` (string, required)
- Query: `timeGte`, `timeLte`

#### 10. Get token price change
- `GET /token/price_change/{id}`
- Path: `id` (string, required)

#### 11. Get top tokens
- `GET /token/top`
- Query: `limit`, `offset`, `chains`

#### 12. Get top token flow by chain/address
- `GET /token/top_flow/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)
- Query: `flow`, `timeLast`, `timeGte`, `timeLte`

#### 13. Get top token flow by ID
- `GET /token/top_flow/{id}`
- Path: `id` (string, required)
- Query: `flow`, `timeLast`, `timeGte`, `timeLte`

#### 14. Get trending tokens
- `GET /token/trending`
- No parameters

#### 15. Get trending token by ID
- `GET /token/trending/{id}`
- Path: `id` (string, required)

#### 16. Get token volume by chain/address
- `GET /token/volume/{chain}/{address}`
- Path: `chain` (string, required), `address` (string, required)
- Query: `timeGte`, `timeLte`

#### 17. Get token volume by ID
- `GET /token/volume/{id}`
- Path: `id` (string, required)
- Query: `timeGte`, `timeLte`

---

### TRANSFERS Resource

#### 1. Get transfers
- `GET /transfers`
- Query: `base`, `chains`, `flow` (`in|out|self|all`), `from`, `to`, `tokens`, `counterparties`, `timeGte`, `timeLte`, `timeLast`, `valueGte`, `valueLte`, `usdGte`, `usdLte`, `sortKey` (`time|value|usd`), `sortDir` (`asc|desc`), `limit` (default 50), `offset` (default 0)
- **Rate limit: 1 request/second**

#### 2. Get transfer histogram (API tier required)
- `GET /transfers/histogram`
- Query: same filter parameters as `/transfers`
- **Requires API tier subscription**

#### 3. Get simple transfer histogram (API tier required)
- `GET /transfers/histogram/simple`
- Query: same filter parameters as `/transfers`
- **Requires API tier subscription**

#### 4. Get transaction by hash
- `GET /transfers/tx/{hash}`
- Path: `hash` (string, required) — transaction hash

---

### TX Resource

#### 1. Get transaction by hash
- `GET /tx/{hash}`
- Path: `hash` (string, required)

---

### USER Resource

#### 1. List user entities
- `GET /user/entities`
- Query: `limit`, `offset`

#### 2. Get user entity by ID
- `GET /user/entities/{id}`
- Path: `id` (string, required)

#### 3. Add address to user entity
- `PUT /user/entities/only_add/{id}`
- Path: `id` (string, required)
- Body: address data

#### 4. List user labels
- `GET /user/labels`
- No parameters

#### 5. Create user label
- `POST /user/labels`
- Body: label data

---

### VOLUME Resource

#### 1. Get volume for address
- `GET /volume/address/{address}`
- Path: `address` (string, required)
- Query: `chains`, `timeGte`, `timeLte`

#### 2. Get volume for entity
- `GET /volume/entity/{entity}`
- Path: `entity` (string, required)
- Query: `chains`, `timeGte`, `timeLte`

---

### WS Resource

#### 1. List active WebSocket connections
- `GET /ws/active_connections`
- No parameters

#### 2. Get WebSocket session info
- `GET /ws/session-info`
- No parameters

#### 3. List WebSocket sessions
- `GET /ws/sessions`
- No parameters

#### 4. Create WebSocket session
- `POST /ws/sessions`
- Returns: `sessionId` for use in `wss://api.arkm.com/ws/transfers?session_id=<sessionId>`

#### 5. Get WebSocket session by ID
- `GET /ws/sessions/{id}`
- Path: `id` (string, required)

#### 6. Delete WebSocket session
- `DELETE /ws/sessions/{id}`
- Path: `id` (string, required)

#### 7. Get WebSocket transfers (live streaming info)
- `GET /ws/transfers`
- Returns connection info for WebSocket streaming
- Query: `session_id` (required), `fresh` (optional boolean)

---

## Input/Output Examples

### Standard GET request
```bash
uv run arkm intelligence address 0x28c6c06298d514db089934071355e5743bf21d60
uv run arkm intelligence address 0x28c6c06298d514db089934071355e5743bf21d60 --chain ethereum --output json
```

### Batch address lookup from file
```bash
uv run arkm intelligence batch-address --input addresses.csv --output results.xlsx
uv run arkm intelligence batch-address --input addresses.jsonl --output results.csv
```

### Transfers with filters
```bash
uv run arkm transfers list --base binance --flow out --time-last 24h --usd-gte 1000000 --limit 10
uv run arkm transfers list --from 0x123abc --to 0x456def --chains ethereum --output json
```

### Token data
```bash
uv run arkm token top --limit 10
uv run arkm token market ethereum
uv run arkm token price-history ethereum 0x6b175474e89094c44da98b954eedeac495271d0f
```

### Portfolio query
```bash
uv run arkm portfolio address 0x28c6c06298d514db089934071355e5743bf21d60 --chains ethereum,bsc
uv run arkm portfolio entity binance --output xlsx
```

### Search
```bash
uv run arkm intelligence search "Vitalik"
```

### Output format flag
All list/get commands accept `--output [json|csv|xlsx]` (default: `xlsx`).  
All list/get commands accept `--save` to write to a timestamped file.

### Batch input file format (CSV)
```csv
address,chain
0x28c6c06298d514db089934071355e5743bf21d60,ethereum
0xabc123...,bsc
```

### Batch input file format (JSONL)
```jsonl
{"address": "0x28c6c06298d514db089934071355e5743bf21d60", "chain": "ethereum"}
{"address": "0xabc123...", "chain": "bsc"}
```

---

## Caching

- Optional response caching using `requests-cache` or file-based cache
- Cache key: `(method, url, sorted query params)`
- Default TTL: 300 seconds (5 minutes) for GET endpoints
- No caching for POST endpoints (batch) or WebSocket endpoints
- `--no-cache` flag to bypass on any command

---

## Rate Limiting

- **Default**: respect `Retry-After` header when 429 is returned
- **Transfers endpoint** (`/transfers`): enforce 1 request/second client-side
- On `429` responses: wait `Retry-After` seconds then retry (counts against retry budget)
- On `500/502/503/504`: retry with exponential backoff (1s → 2s → 4s)

---

## Error Handling

| HTTP Status | Handling |
|---|---|
| 400 | Print error message + body, exit 1 |
| 401 | "Authentication failed — check ARKM_API_KEY", exit 1 |
| 403 | "Access denied — API tier required for this endpoint", exit 1 |
| 404 | "Resource not found", exit 1 |
| 429 | Retry with backoff up to 3 attempts, then exit 1 with rate limit message |
| 500/502/503/504 | Retry with backoff, then exit 1 |
| Connection error | "Network error: {detail}", exit 1 |

All errors write to stderr. Successful data writes to stdout (or file if `--save`).

If `ARKM_API_KEY` is not set, exit immediately with:
```
Error: ARKM_API_KEY environment variable not set. Add it to .env or export it.
```

---

## Logging

- Logger: standard Python `logging`
- Log level: from `ARKM_LOG_LEVEL` env var (default `INFO`)
- Log to stderr only (never pollute stdout data output)
- Log format: `%(asctime)s %(levelname)s %(name)s: %(message)s`
- Log on each request: method, URL, status code, elapsed time
- Log on retry: attempt number, status, wait time
- `--verbose` / `-v` flag overrides log level to `DEBUG` for that invocation

---

## Best Click Practices

- Main group: `@click.group()` named `cli` in `src/cli.py`
- Each resource is a `@click.group()` registered on `cli`
- Each endpoint is a `@click.command()` registered on its resource group
- Use `@click.option()` for all query parameters (never positional for optional params)
- Use `@click.argument()` for required path parameters
- `--output` option on all list/get commands: choices `['json', 'csv', 'xlsx']`, default `xlsx`
- `--save` flag: write output to timestamped file instead of stdout
- `--limit` / `--offset` on all paginated endpoints
- `--verbose` / `-v` flag available on all commands (pass-through to logger)
- Print help text for each command: include the API path and a one-line description
- Use `click.echo()` for all stdout output; `click.echo(..., err=True)` for errors

---

## Makefile & Project Management

```makefile
install:
	uv venv && uv pip install -e ".[dev]"

lint:
	ruff check --fix src/ && ruff format src/

test:
	pytest tests/ -v

validate:
	uv run arkm chains list --output json --limit 1
	uv run arkm token trending --output json
	uv run arkm intelligence entity-types --output json

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

---

## Implementation Checklist

### Project Scaffold
- [ ] `pyproject.toml` with `[project.scripts]` entry `arkm = "src.cli:cli"`
- [ ] `uv` compatible — no `setup.py`
- [ ] `.env.example` with all env vars documented
- [ ] `.gitignore` includes `.env`

### Core Modules
- [ ] `src/config.py` — load env vars, validate `ARKM_API_KEY` on startup
- [ ] `src/client.py` — `requests.Session` with `API-Key` header, retry, timeout
- [ ] `src/output.py` — `format_output(data, format)` supporting `json`, `csv`, `xlsx`
- [ ] `src/batch_processor.py` — read CSV/JSONL, yield rows, call API, collect results
- [ ] `src/logger.py` — configure logging from env + `--verbose` flag

### Commands
- [ ] All 20 resource command files created
- [ ] All 82 endpoints implemented
- [ ] `--output`, `--save`, `--verbose` on all applicable commands
- [ ] Transfers: client-side 1 req/sec rate limiting
- [ ] Intelligence batch: accept `--input` for CSV/JSONL batch files
- [ ] Intelligence enriched batch: accept `--input` for CSV/JSONL batch files

### Downstream Validation (live API)
The generated project must include a validation step that runs read/list commands with a small record cap against the live API to confirm wiring. Use `--limit 10` (or equivalent) on paginated GET endpoints. Suggested validation targets:
```bash
uv run arkm chains list                                          # no auth required
uv run arkm token trending                                       # no params
uv run arkm intelligence entity-types                            # no params
uv run arkm intelligence search "binance" --output json          # search
uv run arkm transfers list --limit 5                             # rate-limited endpoint
```

These must return 2xx responses (or 403 for API-tier-only endpoints) to count as passing.

### Quality Gates
- [ ] `ruff check --fix src/` passes with zero errors
- [ ] `ruff format src/` produces no changes
- [ ] `pytest tests/` passes
- [ ] All validation commands above return expected status codes
