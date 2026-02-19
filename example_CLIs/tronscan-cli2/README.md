# tronscan-cli

Python CLI client for **Tronscan API** — the TRON blockchain explorer for querying accounts, blocks, and contracts.

**Base URL:** `https://apilist.tronscanapi.com`

---

## Installation

```bash
uv sync
```

> Or with pip: `pip install -r requirements.txt`

## Configuration

```bash
cp .env.example .env
```

Required environment variables:

```env
TRONSCAN_API_KEY=your-tron-pro-api-key-here
```

Full options: see `.env.example`.

---

## Help

```
Usage: tronscan [OPTIONS] COMMAND [ARGS]...

  tronscan — TRON blockchain explorer CLI.

  Queries the Tronscan API (https://apilist.tronscanapi.com) for account,
  block, and contract data.

  Quick start:
    tronscan accounts list --limit 20
    tronscan blocks stats
    tronscan contracts list --search USDT

Options:
  --version       Show the version and exit.
  --api-key TEXT  Tronscan API key (TRON-PRO-API-KEY).
  --verbose       Enable DEBUG-level output.
  --help          Show this message and exit.

Commands:
  accounts   TRON account operations.
  batch      Process a TXT (JSON Lines) batch file and save results to XLSX.
  blocks     TRON blockchain block data.
  contracts  TRON smart contract operations.
```

### Resource commands

```
Usage: tronscan accounts [OPTIONS] COMMAND [ARGS]...

  TRON account operations.

Commands:
  get     Get comprehensive account details.
  list    List TRON accounts with pagination.
  tokens  List tokens held by an account.
```

```
Usage: tronscan blocks [OPTIONS] COMMAND [ARGS]...

  TRON blockchain block data.

Commands:
  list   List TRON blocks with optional producer/timestamp filters.
  stats  Get block statistical summary (burn, count, last day pay).
```

```
Usage: tronscan contracts [OPTIONS] COMMAND [ARGS]...

  TRON smart contract operations.

Commands:
  events  Get event logs for a contract (batch endpoint).
  get     Get comprehensive details for a specific smart contract.
  list    List smart contracts with optional search and filter.
```

---

## Batch Processing

Input file format — `data/batch.txt`, one JSON object per line:

```jsonl
{"command": "accounts-list", "limit": 5, "sort": "-balance"}
{"command": "accounts-get", "address": "TAddr..."}
{"command": "accounts-tokens", "address": "TAddr...", "limit": 20}
{"command": "blocks-list", "limit": 10}
{"command": "blocks-stats"}
{"command": "contracts-list", "search": "USDT", "limit": 5}
{"command": "contracts-get", "contract": "TAddr..."}
{"command": "contracts-events", "contract_address": "TAddr...", "term": "Transfer", "limit": 50}
```

```bash
tronscan batch --input-file data/batch.txt --output-dir output/
```

Output: `output/batch_results_YYYYMMDD_HHMMSS.xlsx` — sheets: Summary, Results, Errors.

---

## Development

```
tronscan-cli — Available commands:

  Setup:
    make install           Install dependencies (uv sync)
    make install-dev       Install with dev dependencies

  Development:
    make lint              Run linters (black + pylint)
    make format            Format code (black + isort)
    make test              Run tests
    make test-cov          Run tests with coverage
    make clean             Clean build artifacts

  Accounts:
    make accounts-list     List top accounts by balance
    make accounts-get      Get account details (ADDRESS=...)
    make accounts-tokens   List account tokens (ADDRESS=...)

  Blocks:
    make blocks-list       List latest blocks
    make blocks-stats      Get block statistics

  Contracts:
    make contracts-list    List smart contracts
    make contracts-get     Get contract details (CONTRACT=...)
    make contracts-events  Get contract events (CONTRACT=...)

  Batch:
    make batch             Run batch from data/batch.txt
```

---

## Project Structure

```
.
├── data
│   └── batch.txt
├── src
│   ├── commands
│   │   ├── accounts_commands.py
│   │   ├── blocks_commands.py
│   │   ├── contracts_commands.py
│   │   └── __init__.py
│   ├── batch_processor.py
│   ├── client.py
│   ├── cli.py
│   ├── config.py
│   ├── __init__.py
│   ├── logger.py
│   └── output.py
├── tests
│   ├── __init__.py
│   └── test_cli.py
├── .env.example
├── Makefile
├── pyproject.toml
└── requirements.txt
```

---

## API Reference

**Authentication:** `TRON-PRO-API-KEY` header

Full endpoint reference: [`tronscan-prd.md`](../../example_PRDs/tronscan-prd.md)
