# tronscan-cli

Python CLI client for **Tronscan API** — the TRON blockchain explorer for querying accounts, blocks, and contracts.

## Installation

```bash
# Install dependencies
uv sync

# Or with pip
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:

```env
TRONSCAN_API_KEY=your-tron-pro-api-key-here
```

## Usage

```bash
# Show all commands
tronscan --help

# Resource commands
tronscan accounts list --limit 20 --sort -balance
tronscan accounts get --address TAddr...
tronscan accounts tokens --address TAddr...

tronscan blocks list --limit 20
tronscan blocks stats

tronscan contracts list --search USDT
tronscan contracts get --contract TAddr...
tronscan contracts events --contract-address TAddr... --term Transfer

# Enable debug output
tronscan --verbose accounts list
```

## Resources

- **accounts** — TRON account operations
  - `list` — Paginated list of accounts, sortable by balance
  - `get` — Full account details by address
  - `tokens` — Token holdings for an account

- **blocks** — TRON blockchain block data
  - `list` — Paginated blocks, filterable by producer / timestamp
  - `stats` — Summary statistics (burn, count, last day pay)

- **contracts** — TRON smart contract operations
  - `list` — Searchable contract directory
  - `get` — Full contract details by address
  - `events` — Event logs via batch endpoint (POST)

## Batch Processing

Place a `.txt` file in `data/` with one JSON object per line:

```jsonl
{"command": "accounts-list", "limit": 5, "sort": "-balance"}
{"command": "accounts-get", "address": "TAddr..."}
{"command": "blocks-list", "limit": 10}
{"command": "blocks-stats"}
{"command": "contracts-list", "search": "USDT", "limit": 5}
{"command": "contracts-get", "contract": "TAddr..."}
{"command": "contracts-events", "contract_address": "TAddr...", "term": "Transfer", "limit": 50}
```

Run the batch:

```bash
tronscan batch --input-file data/batch.txt --output-dir output/
```

Results are saved to `output/batch_results_YYYYMMDD_HHMMSS.xlsx` with three sheets: Summary, Results, Errors.

## Development

```bash
make install-dev   # Install with dev dependencies
make lint          # Run linters
make format        # Format code
make test          # Run tests
make help          # Show all Makefile targets
```

## Project Structure

```
tronscan-cli/
├── src/
│   ├── cli.py                  # CLI entry point
│   ├── client.py               # httpx client (TRON-PRO-API-KEY auth, retry)
│   ├── config.py               # Configuration from .env
│   ├── logger.py               # Screen logging
│   ├── output.py               # XLSX output via pandas + openpyxl
│   ├── batch_processor.py      # TXT (JSON Lines) batch runner
│   └── commands/
│       ├── accounts_commands.py
│       ├── blocks_commands.py
│       └── contracts_commands.py
├── data/                       # Batch input files
├── output/                     # Generated XLSX output
├── tests/
├── Makefile
├── pyproject.toml
└── .env.example
```

## API Reference

**Base URL:** `https://apilist.tronscanapi.com`

**Authentication:** `TRON-PRO-API-KEY` header

Full endpoint reference: see `../../example_PRDs/tronscan-prd.md`
