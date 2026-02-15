# Tronscan API Python CLI

A production-ready Python CLI for querying the TRON blockchain via Tronscan API.

**Features:**
- 🔐 Query accounts, transactions, blocks, smart contracts, tokens, and network data
- 📦 Batch processing from CSV files
- 💾 Multiple output formats (JSON, XLSX)
- ⚡ Async HTTP client with automatic retry logic
- 🔄 Connection pooling and performance optimization
- ⏰ Timestamp-based output file naming
- 📝 Comprehensive logging

---

## Installation

### 1. Clone or create the project

```bash
cd tronscan-cli
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API key

```bash
cp .env.example .env
# Edit .env and add your Tronscan API key
```

Get an API key from: https://tronscan.org (Settings → API)

---

## Usage

### Quick Start

```bash
# Get account information
python -m src.cli accounts info --address TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L

# List transactions
python -m src.cli transactions list --start 0 --limit 10

# Get blockchain statistics
python -m src.cli network stats

# Process batch requests
python -m src.cli batch --input-file data/requests.csv --format json
```

### Commands

#### Accounts
```bash
python -m src.cli accounts info --address TRONSCAN_ADDRESS
python -m src.cli accounts votes --address TRONSCAN_ADDRESS
python -m src.cli accounts list --start 0 --limit 20
```

#### Transactions
```bash
python -m src.cli transactions info --hash TX_HASH
python -m src.cli transactions count
python -m src.cli transactions list --start 0 --limit 20
python -m src.cli transactions stats
```

#### Blocks
```bash
python -m src.cli blocks info --number BLOCK_NUMBER
python -m src.cli blocks list --start 0 --limit 20
python -m src.cli blocks count
```

#### Smart Contracts
```bash
python -m src.cli smartcontracts info --address CONTRACT_ADDRESS
python -m src.cli smartcontracts list --start 0 --limit 20
```

#### Transfers
```bash
python -m src.cli transfers info --hash TRANSFER_HASH
python -m src.cli transfers list --start 0 --limit 20
```

#### Tokens
```bash
python -m src.cli tokens info --address TOKEN_ADDRESS
python -m src.cli tokens list --start 0 --limit 20
```

#### Network
```bash
python -m src.cli network parameters
python -m src.cli network stats
```

#### Batch Processing
```bash
python -m src.cli batch \
  --input-file data/requests.csv \
  --format json \
  --output-path output \
  --include-timestamp
```

---

## Configuration

### .env File

Required settings:
- `TRONSCAN_API_KEY`: Your API key from Tronscan
- `TRONSCAN_BASE_URL`: API base URL (default: https://apilist.tronscan.org)

Optional settings:
- `TRONSCAN_TIMEOUT`: Request timeout in seconds (default: 30)
- `TRONSCAN_RETRIES`: Max retry attempts (default: 3)
- `TRONSCAN_RETRY_DELAY`: Initial retry delay in seconds (default: 1)
- `TRONSCAN_LOG_LEVEL`: Logging level - DEBUG, INFO, WARNING, ERROR (default: INFO)

### Logging

Logs are saved to `tronscan_cli.log` and printed to console.

Enable debug logging:
```bash
python -m src.cli --verbose accounts info --address ...
```

---

## Batch Processing

### CSV Input Format

Create `data/requests.csv`:

```csv
method,endpoint,address
GET,/api/account,TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L
GET,/api/account,TJzzWvwj8WJnhHa2H8QJgKvfAPXqnwXUHz
GET,/api/token,TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L
```

### Process Batch

```bash
python -m src.cli batch \
  --input-file data/requests.csv \
  --format json \
  --include-timestamp
```

Results are saved to `output/results_20260215_143022.json`

### Output Formats

- **JSON** (default): Structured data with full responses
- **XLSX**: Excel spreadsheet with flattened data (integers, no index)

---

## Project Structure

```
tronscan-cli/
├── src/
│   ├── __init__.py              # Package init
│   ├── cli.py                   # Main CLI entry point
│   ├── config.py                # Configuration management
│   ├── client.py                # HTTP client with retry logic
│   ├── batch_processor.py       # Batch request processing
│   └── commands/
│       ├── __init__.py
│       ├── accounts_commands.py    # Account queries
│       ├── transactions_commands.py # Transaction queries
│       ├── blocks_commands.py      # Block queries
│       ├── smartcontracts_commands.py  # Smart contract queries
│       ├── transfers_commands.py   # Transfer queries
│       ├── tokens_commands.py      # Token queries
│       └── network_commands.py     # Network queries
├── data/                        # Batch input files directory
├── output/                      # Results directory
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
├── .env                         # Your configuration (git-ignored)
└── tronscan_cli.log            # Application logs
```

---

## Error Handling

The CLI automatically handles common errors:

- **401 Unauthorized**: Check your API key in `.env`
- **429 Too Many Requests**: Automatic retry with exponential backoff
- **500-504 Errors**: Automatic retry with jitter
- **Network timeout**: Configurable via `TRONSCAN_TIMEOUT`

All errors are logged to `tronscan_cli.log`.

---

## Performance Tips

1. **Batch Processing**: Use batch mode for multiple queries instead of individual commands
2. **Pagination**: Use `--limit 200` for faster list operations (max allowed)
3. **Connection Pooling**: The client reuses connections automatically
4. **Rate Limiting**: Built-in 100ms delay between requests respects API limits

---

## Development

### Run Tests (if available)

```bash
pytest tests/
```

### Modify Commands

Edit files in `src/commands/` to add or modify commands:

```python
@resource.command()
@click.option('--option', required=True)
@click.pass_context
def my_command(ctx, option):
    """Command description."""
    client = ctx.obj["client"]
    # Your code here
```

### Add New Resource

1. Create `src/commands/newresource_commands.py`
2. Define command group and commands
3. Import and add to `src/cli.py`:

```python
from .commands.newresource_commands import newresource
cli.add_command(newresource)
```

---

## Troubleshooting

### API key not working
- Verify API key is in `.env`
- Check key hasn't expired on Tronscan dashboard
- Restart CLI after updating .env

### Batch processing errors
- Ensure CSV file has correct columns: `method`, `endpoint`, parameters
- Check file path is correct and readable
- Enable `--verbose` flag to see detailed errors

### Slow responses
- Check network connectivity
- Increase `TRONSCAN_TIMEOUT` if requests are timing out
- Try with smaller `--limit` values for list operations

---

## Support

- **Tronscan API Docs**: https://tronscan.org
- **TRON Network**: https://tron.network
- **Issues**: Create an issue or check logs in `tronscan_cli.log`

---

**Generated**: 2026-02-15
**Version**: 1.0.0
**License**: Apache 2.0
