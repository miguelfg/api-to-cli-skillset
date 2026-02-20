---
name: prd-to-cli
description: Generate a production-ready Python Click CLI project from a PRD.md file about an API. Takes a Product Requirements Document describing an API client and generates a complete project structure with one Click subcommand per API resource, batch request processing (CSV/TXT), configuration management (.env), and output formatting options (JSON/CSV/XLSX). Uses askUserQuestion to gather user preferences for batch input formats, output destination, file formats, and timestamp configurations. Use when converting API documentation into an executable CLI tool.
triggers:
  - User provides a PRD.md and requests code generation for a Python Click CLI.
  - User asks to scaffold a production-ready API CLI project from requirements.
  - User completed `doc-to-prd` and wants the final generated CLI project structure.
do_not_trigger_when:
  mode: intent
  conditions:
    - Required input is missing (no PRD path/content provided).
    - User intent is explanation, review, or discussion only (no code/project generation requested).
    - User asks only to edit or refine PRD content (use `doc-to-prd` or direct PRD editing flow).
    - Request is ambiguous about target artifact and user has not confirmed intent.
---

# PRD to Python Click CLI Generator

Generate production-ready Python Click CLI projects from API documentation PRD.md files. The skill parses your PRD, extracts API resources and endpoints, then generates a complete project with one subcommand per resource, batch processing capabilities, and configurable output formats.

## Expected Parameters

```
/prd-to-cli <PRD_FILE_PATH> <OUTPUT_FOLDER>
```

**Parameters:**
- `PRD_FILE_PATH` (required): Path to the PRD.md file
  - Example: `/prd-to-cli @path/to/PRD.md`
- `OUTPUT_FOLDER` (required): Directory where the generated CLI project will be created
  - Example: `/prd-to-cli @PRD.md ./projects`

**Interactive Configuration:**
The skill will prompt for:
- Project name
- HTTP library choice (requests, httpx, aiohttp, etc.). Default: `requests`
- Logging preferences (screen only, file only, both, none). Default: screen only
- Batch input (yes/no, CSV/TXT/both). Default: both
- Output formats (JSON, CSV, XLSX, multiple selection). Default: XLSX
- Timestamp configuration (format and inclusion in filenames)

**Output:** Complete project structure in the specified output folder

## Quick Start

Invoke the skill with a PRD.md file path:

```
/prd-to-cli @path/to/PRD.md
```

The skill will:
1. **Ask questions** via `askUserQuestion` about:
   - HTTP library (requests, httpx, aiohttp, etc.)
   - Batch input formats (CSV, TXT, or both)
   - Project name and output directory
   - Logging preferences (screen, file, both, none)
   - Output format preferences (JSON, CSV, XLSX)
   - Timestamp configuration (format, include in filenames)
   - .env configuration options

2. **Generate project structure:**
   - `src/cli.py` — Main Click CLI entry point
   - `src/commands/{resource}_commands.py` — One file per API resource
   - `src/client.py` — HTTP client wrapper (using selected library)
   - `src/config.py` — Configuration management
   - `src/batch_processor.py` — Batch request processor
   - `src/logger.py` — Logging configuration helpers
   - `src/output.py` — Output export helpers (JSON/CSV/XLSX)
   - `src/utils.py` — Shared parsing/util functions
   - `Makefile` — Development commands and endpoint examples
   - `tests/test_cli.py` — Basic CLI smoke tests
   - `README.md` — Project documentation (from `assets/README_template.md`)
   - `.env.example` — Configuration template
   - `pyproject.toml` — Project metadata and console script entry point
   - `requirements.txt` — Dependencies
   - `logs/` — Log directory (if file logging enabled)
   - `data/` and `output/` — Data directories

3. **Support batch processing:**
   - Accept CSV format: `method,endpoint,param1,param2`
   - Accept TXT format (JSON Lines): one request per line
   - Process and save results with configurable timestamp

## Workflow

### Step 1: Provide PRD File

Ensure your PRD.md has these sections:

**API Metadata:**
```markdown
# PRD: Petstore API Python Client
**API Version:** 1.0.7
**Base URL:** https://petstore.swagger.io/v2
```

**API Resources** (section headers):
```markdown
### PETS Resource
#### 1. Get Pet by ID
#### 2. List Pets by Status
...

### ORDERS Resource
#### 1. Place Order
#### 2. Get Order by ID
...

### USERS Resource
#### 1. Create User
...
```

### Step 2: User Configuration Questions

When you invoke the skill, it asks:

**Question 1:** Which batch input formats to accept?
- CSV only
- TXT (JSON Lines) only
- Both CSV and TXT

**Question 2:** Project details?
- Project name (becomes CLI command)
- Output directory path

**Question 3:** Output format preferences?
- JSON (default)
- CSV (tabular export)
- XLSX (Excel export)
- Multiple formats

**Question 4:** Timestamp configuration?
- Include timestamp in output filenames?
- Timestamp format: `YYYYMMDD_HHMMSS` (default)

### Step 3: Project Generation

The skill generates a complete project with CLI structure matching your PRD resources.

**Example PRD sections:**
```markdown
### PETS Resource
### ORDERS Resource
### USERS Resource
```

**Generated commands:**
```bash
python -m src.cli pets list
python -m src.cli orders create --data '...'
python -m src.cli users get --username john
python -m src.cli batch --input-file data/batch.csv
```

### Step 4: Batch Processing

Users create batch files in the `data/` directory:

**CSV format** (`data/pets-batch.csv`):
```csv
method,endpoint,name,status
GET,/pet/findByStatus,available
POST,/pet,Fluffy,available
DELETE,/pet/1
```

**TXT format** (`data/users-batch.txt`):
```json
{"method": "POST", "endpoint": "/user", "username": "john"}
{"method": "GET", "endpoint": "/user/john"}
```

**Process batch:**
```bash
python -m src.cli batch \
  --input-file data/pets-batch.csv \
  --format json \
  --output-path ./output \
  --include-timestamp
```

**Results saved:** `output/results_20260215_143022.json`

---

## Key Features

✨ **One subcommand per resource** — Extract resources from PRD, create corresponding CLI commands
📝 **Batch processing** — Accept CSV or TXT (JSON Lines) input files
💾 **Multiple output formats** — JSON, CSV, XLSX with configurable paths
⏰ **Timestamp support** — Include or exclude timestamps in filenames
⚙️ **.env configuration** — Secure API key and settings management
🔄 **Configurable options** — Ask users about preferences, not hardcoded
🐍 **HTTP library selection** — Choose between requests, httpx, aiohttp, etc.
📋 **Makefile generation** — Standard development commands and endpoint examples
📊 **Smart output flattening** — Flatten nested JSON with dot notation
🗂️ **XLSX split sheets** — Automatically split nested data to separate sheets
🪵 **Flexible logging** — Screen, file, or both with timestamp patterns

---

## HTTP Library Selection

Users can choose their preferred Python HTTP library during project generation:

**Supported libraries:**
- `requests` (default) — Synchronous, most popular
- `httpx` — Modern, async-capable, requests-compatible
- `aiohttp` — Fully async, high performance
- `urllib3` — Lightweight, batteries-included

The generated `src/client.py` and `requirements.txt` are configured for the selected library.

---

## Makefile Integration

Generated projects include a `Makefile` with common development tasks:

**Standard targets:**
```bash
make install      # Install dependencies
make install-dev  # Install with dev dependencies
make lint         # Run code linting
make format       # Format code
make test         # Run tests
```

**Endpoint example targets** (auto-generated):
```bash
make accounts-get      # GET /accounts/{id}
make accounts-list     # GET /accounts
make accounts-create   # POST /accounts
make transactions-get  # GET /transactions/{id}
make users-update      # PUT /users/{id}
```

Each endpoint target calls the CLI with example parameters for quick testing.

---

## Logging Configuration

Generated projects support flexible logging:

**Default:** Screen-only logging

**Options:**
- **Screen only** — Console output (default)
- **File only** — Write to `logs/{cli-name}_{timestamp}.log`
- **Both** — Console + file logging
- **None** — No logging

**Log file pattern:**
```
logs/
├── tronscan_cli_20240115_143022.log
├── tronscan_cli_20240115_150000.log
└── tronscan_cli_20240116_091500.log
```

Configuration in `.env`:
```
LOG_LEVEL=INFO
LOG_TO_FILE=true
```

---

## Smart Output Flattening (JSON)

When endpoints return nested entities, JSON output is automatically flattened using dot notation:

**API Response:**
```json
{
  "data": {
    "id": 123,
    "name": "Example",
    "details": {
      "field1": "value1",
      "field2": "value2"
    }
  }
}
```

**Flattened JSON output (`accounts.json`):**
```json
{
  "id": 123,
  "name": "Example",
  "details.field1": "value1",
  "details.field2": "value2"
}
```

Benefits:
- ✓ Works naturally with CSV export
- ✓ Easier filtering and searching
- ✓ Database-friendly format
- ✓ Flat structure preserves all information

---

## XLSX Split Sheets

When outputting to XLSX with nested data, tables are automatically split to separate sheets:

**API Response with nested entities:**
```json
{
  "accounts": [
    {
      "id": 123,
      "name": "Example",
      "details": {
        "field1": "value1",
        "field2": "value2"
      }
    }
  ]
}
```

**Generated XLSX structure:**

**Sheet 1 - accounts (main entity):**
| id  | name    |
| --- | ------- |
| 123 | Example |

**Sheet 2 - account_details (nested relationship):**
| account_id | field1 | field2 |
| ---------- | ------ | ------ |
| 123        | value1 | value2 |

**How it works:**
- Main entities in first sheet
- Each nested object gets its own sheet
- Foreign key references maintain relationships
- Sheet names derived from data structure

Benefits:
- ✓ Normalized structure
- ✓ Easier data analysis in Excel
- ✓ Avoids data duplication
- ✓ Supports multiple nested levels

---

## Logging Configuration Examples

**Default (screen only):**
```
INFO: GET /accounts - 0.45s
INFO: Response: 5 records returned
INFO: Cache: MISS
```

**File logging:**
```
logs/tronscan_cli_20240115_143022.log:
2024-01-15 14:30:22 INFO GET /accounts - 0.45s
2024-01-15 14:30:23 INFO Response: 5 records returned
2024-01-15 14:30:24 INFO Cache: MISS
```

**Debug mode (--verbose):**
```
DEBUG: Request URL: https://api.example.com/accounts
DEBUG: Request Headers: {"Authorization": "Bearer..."}
DEBUG: Response Status: 200
DEBUG: Response Body: {...full JSON...}
INFO: Processing completed in 1.23s
```

---

## Project Structure Example

**Generated project with all new features:**

```
tronscan_cli/
├── Makefile                    # Development commands + endpoints
├── src/
│   ├── cli.py
│   ├── client.py               # Uses selected HTTP library
│   ├── config.py
│   ├── logger.py               # Logging configuration
│   ├── output.py               # Output helpers
│   ├── utils.py                # Shared utilities
│   ├── batch_processor.py
│   └── commands/
│       ├── accounts_commands.py
│       └── transactions_commands.py
├── tests/
│   └── test_cli.py
├── logs/                        # Created if file logging enabled
│   └── tronscan_cli_*.log
├── data/
├── output/
├── .env
├── .env.example
└── requirements.txt             # Includes selected HTTP library
```

**Usage:**
```bash
# Install with selected HTTP library
make install

# Run endpoint examples
make accounts-list
make transactions-get

# Enable debug logging
export LOG_LEVEL=DEBUG
tronscan-cli accounts list --verbose

# Batch processing with smart output
tronscan-cli batch --input data/batch.csv --format json --output output/
# → Flattened JSON in output/results_*.json

tronscan-cli batch --input data/batch.csv --format xlsx --output output/
# → Split sheets in output/results_*.xlsx
```

---

## Reference Materials

**[input_format_specs.md](references/input_format_specs.md)** — CSV and TXT (JSON Lines) format specifications with examples

**[output_configuration.md](references/output_configuration.md)** — Output format options, .env configuration, timestamp formats, command-line usage

**[generated_structure.md](references/generated_structure.md)** — Full project structure, file descriptions, customization points, quick start guide

Refer to these when understanding input requirements, configuring outputs, or working with the generated project.

---

## Example: Petstore API

**Input:** `PRD.md` with sections like:
```markdown
### PETS Resource
### ORDERS Resource
### USERS Resource
```

**User configuration:**
- Formats: CSV and TXT
- Project name: `petstore_client`
- Output formats: JSON and XLSX
- Timestamp: Include with format `%Y%m%d_%H%M%S`

**Generated project:**
```
petstore_client/
├── src/
│   ├── cli.py
│   ├── commands/
│   │   ├── pets_commands.py
│   │   ├── orders_commands.py
│   │   └── users_commands.py
│   ├── client.py
│   ├── config.py
│   └── batch_processor.py
├── data/
├── output/
├── .env
├── requirements.txt
├── pyproject.toml
```

**Usage:**
```bash
# Individual commands
python -m src.cli pets list
python -m src.cli orders create
python -m src.cli users get

# Batch processing
python -m src.cli batch --input-file data/pets.csv --format json --include-timestamp
```

---

## Resource Files

**`scripts/generate_cli_from_prd.py`** — Main generation script that:
- Parses PRD.md to extract API resources
- Generates full project structure
- Creates Click command files for each resource
- Sets up batch processing and configuration

**Assets**:
- `assets/README_template.md` — Generated project README base template
- `assets/pyproject_template.toml` — `pyproject.toml` template included in generated projects
- `assets/config_template.py` — `src/config.py` template
- `assets/logger_template.py` — `src/logger.py` template
- `assets/output_template.py` — `src/output.py` template
- `assets/utils_template.py` — `src/utils.py` template
- `assets/test_cli_template.py` — `tests/test_cli.py` template
- `assets/makefile_template.mk` — `Makefile` template

**References** — Configuration and specification guides for users of generated projects

## Next Possible Steps

Pipeline continuation from this final generation step:

1. Smoke-test generated CLI commands:
```bash
python -m src.cli --help
```
2. Run project tests (if present):
```bash
pytest tests/ -v
```
3. Iterate upstream artifacts when needed:
```bash
/doc-to-prd @<project-name>-api.yaml
```
