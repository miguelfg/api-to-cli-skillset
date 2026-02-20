# PRD: Arkham Intel API Python CLI Client

**API Version:** 1.1.0
**Base URL:** https://api.arkm.com
**Source Spec:** `example_APIs/arkm-intel-api-v1/openapi.yaml`
**Resources:** `arkm, balances, chains, cluster, counterparties, flow, history, intelligence, loans, marketdata, networks, portfolio, swaps, tag, token, transfers, tx, user, volume, ws`

## Introduction

### Overview
Build a production-ready Python CLI client for **Arkham Intel API** with resource-oriented commands, batch processing, and structured output formats.

### Purpose
- Provide a consistent command-line interface for Arkham Intel API endpoints.
- Support single-call and batch workflows.
- Produce machine-readable outputs for downstream automation.

## Implementation Decisions

- CLI Name: `arkm-cli`
- Python Version: `>=3.10`
- HTTP Library: `requests`
- Authentication: `api_key` header
- Credential Sources: `.env, config`
- Timeout: `30s total timeout`
- Retry Policy: `3 attempts, exponential backoff (1s, 2s, 4s) on 408/429/5xx`
- Output Formats: `json,csv,xlsx`
- Batch Input Formats: `csv|txt`
- Timestamped Outputs: `yes (%Y%m%d_%H%M%S)`
- Lint/Format Toolchain: `ruff check --fix` + `ruff format`
- Validation Commands: `make install; uv run arkm-cli --help; make <resource>-list`

## Installation

### Requirements
- Python 3.10+
- `uv`

### Commands
```bash
uv sync
uv run arkm-cli --help
```

## Configuration

Environment variables:
```env
ARKHAM_INTEL_API_API_KEY=<your_api_key>
ARKHAM_INTEL_API_BASE_URL=https://api.arkm.com
ARKHAM_INTEL_API_TIMEOUT=30
```

## Authentication

Use API key authentication through request headers. Exact header name and scope should follow provider docs.

## Endpoint Reference

### Resource Inventory
- `arkm`
- `balances`
- `chains`
- `cluster`
- `counterparties`
- `flow`
- `history`
- `intelligence`
- `loans`
- `marketdata`
- `networks`
- `portfolio`
- `swaps`
- `tag`
- `token`
- `transfers`
- `tx`
- `user`
- `volume`
- `ws`

### Endpoint Inventory
- `/arkm/circulating` — GET
- `/balances/address/{address}` — GET
- `/balances/entity/{entity}` — GET
- `/balances/solana/subaccounts/address/{addresses}` — GET
- `/balances/solana/subaccounts/entity/{entities}` — GET
- `/chains` — GET
- `/cluster/{id}/summary` — GET
- `/counterparties/address/{address}` — GET
- `/counterparties/entity/{entity}` — GET
- `/flow/address/{address}` — GET
- `/flow/entity/{entity}` — GET
- `/history/address/{address}` — GET
- `/history/entity/{entity}` — GET
- `/intelligence/address/batch` — POST
- `/intelligence/address/batch/all` — POST
- `/intelligence/address/{address}` — GET
- `/intelligence/address/{address}/all` — GET
- `/intelligence/address_enriched/batch` — POST
- `/intelligence/address_enriched/batch/all` — POST
- `/intelligence/address_enriched/{address}` — GET
- `/intelligence/address_enriched/{address}/all` — GET
- `/intelligence/address_tags/updates` — GET
- `/intelligence/addresses/updates` — GET
- `/intelligence/contract/{chain}/{address}` — GET
- `/intelligence/entities/updates` — GET
- `/intelligence/entity/{entity}` — GET
- `/intelligence/entity/{entity}/summary` — GET
- `/intelligence/entity_balance_changes` — GET
- `/intelligence/entity_predictions/{entity}` — GET
- `/intelligence/entity_types` — GET
- `/intelligence/search` — GET
- `/intelligence/tags/updates` — GET
- `/intelligence/token/{chain}/{address}` — GET
- `/intelligence/token/{id}` — GET
- `/loans/address/{address}` — GET
- `/loans/entity/{entity}` — GET
- `/marketdata/altcoin_index` — GET
- `/networks/history/{chain}` — GET
- `/networks/status` — GET
- `/portfolio/address/{address}` — GET
- `/portfolio/entity/{entity}` — GET
- `/portfolio/timeSeries/address/{address}` — GET
- `/portfolio/timeSeries/entity/{entity}` — GET
- `/swaps` — GET
- `/tag/{id}/params` — GET
- `/tag/{id}/summary` — GET
- `/token/addresses/{id}` — GET
- `/token/arkham_exchange_tokens` — GET
- `/token/balance/{chain}/{address}` — GET
- `/token/balance/{id}` — GET
- `/token/holders/{chain}/{address}` — GET
- `/token/holders/{id}` — GET
- `/token/market/{id}` — GET
- `/token/price/history/{chain}/{address}` — GET
- `/token/price/history/{id}` — GET
- `/token/price_change/{id}` — GET
- `/token/top` — GET
- `/token/top_flow/{chain}/{address}` — GET
- `/token/top_flow/{id}` — GET
- `/token/trending` — GET
- `/token/trending/{id}` — GET
- `/token/volume/{chain}/{address}` — GET
- `/token/volume/{id}` — GET
- `/transfers` — GET
- `/transfers/histogram` — GET
- `/transfers/histogram/simple` — GET
- `/transfers/tx/{hash}` — GET
- `/tx/{hash}` — GET
- `/user/entities` — GET
- `/user/entities/only_add/{id}` — PUT
- `/user/entities/{id}` — GET
- `/user/labels` — GET, POST
- `/volume/address/{address}` — GET
- `/volume/entity/{entity}` — GET
- `/ws/active_connections` — GET
- `/ws/session-info` — GET
- `/ws/sessions` — GET, POST
- `/ws/sessions/{id}` — DELETE, GET
- `/ws/transfers` — GET

## CLI Design

Command shape:
```bash
uv run arkm-cli <resource> <command> [options]
```

Examples:
```bash
uv run arkm-cli balances list --address <wallet>
uv run arkm-cli intelligence search --query "entity"
uv run arkm-cli batch --input-file data/batch.csv --format json
```

## Input/Output Examples

### Input
- Single request via command options
- Batch input via CSV or JSONL/TXT

### Output
- `json` for API-native payloads
- `csv` for tabular extracts
- `xlsx` for analyst workflows

## Error Handling

- 4xx: surface actionable validation/auth messages
- 429: retry with backoff and preserve context
- 5xx/network: retry with capped attempts; fail with structured error output

## Logging

- Default `INFO`, optional `DEBUG` via `--verbose`
- Include timestamp, endpoint, status code, and duration

## Makefile & Project Management

Contract:
- Runtime commands must use `uv run arkm-cli ...`
- Project installation must use `uv sync`
- Final Makefile targets are owned by `prd-to-cli`

## Next Possible Steps

1. Generate CLI project:
```bash
/prd-to-cli @example_PRDs/arkham_intel_api_PRD.md example_CLIs/arkm-cli
```
2. Validate generated CLI:
```bash
make install
uv run arkm-cli --help
```
