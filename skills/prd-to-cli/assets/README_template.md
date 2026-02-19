# [PROJECT_NAME]

Python CLI client for **[API_NAME]**.

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
[API_PREFIX]_API_KEY=your-api-key-here
```

## Usage

```bash
# Show all commands
[CLI_NAME] --help

# Resource commands
[RESOURCE_COMMAND_EXAMPLES]

# Enable debug output
[CLI_NAME] --verbose [RESOURCE] [COMMAND]
```

## Resources

[RESOURCE_LIST]

## Batch Processing

Place a `.txt` file in `data/` with one JSON object per line:

```jsonl
[BATCH_EXAMPLES]
```

Run the batch:

```bash
[CLI_NAME] batch --input-file data/batch.txt --output-dir output/
```

Results are saved to `output/batch_results_YYYYMMDD_HHMMSS.xlsx`.

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
[PROJECT_NAME]/
├── src/
│   ├── cli.py                  # CLI entry point
│   ├── client.py               # HTTP client
│   ├── config.py               # Configuration
│   ├── logger.py               # Logging
│   ├── output.py               # Output formatting (XLSX)
│   ├── batch_processor.py      # Batch runner
│   └── commands/
│       [COMMAND_FILES]
├── data/                       # Batch input files
├── output/                     # Generated output files
├── tests/
├── Makefile
├── pyproject.toml
└── .env.example
```

## API Reference

**Base URL:** `[BASE_URL]`

**Authentication:** `[AUTH_HEADER]` header

Full endpoint reference: see `[PRD_PATH]`
