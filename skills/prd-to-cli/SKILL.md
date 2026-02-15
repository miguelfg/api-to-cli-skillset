---
name: prd-to-cli
description: Generate a production-ready Python Click CLI project from a PRD.md file about an API. Takes a Product Requirements Document describing an API client and generates a complete project structure with one Click subcommand per API resource, batch request processing (CSV/TXT), configuration management (.env), and output formatting options (JSON/CSV/XLSX). Uses askUserQuestion to gather user preferences for batch input formats, output destination, file formats, and timestamp configurations. Use when converting API documentation into an executable CLI tool.
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
- Batch input formats (CSV, TXT, or both)
- Output formats (JSON, CSV, XLSX)
- Timestamp configuration (format and inclusion in filenames)

**Output:** Complete project structure in the specified output folder

## Quick Start

Invoke the skill with a PRD.md file path:

```
/prd-to-cli @path/to/PRD.md
```

The skill will:
1. **Ask questions** via `askUserQuestion` about:
   - Batch input formats (CSV, TXT, or both)
   - Project name and output directory
   - Output format preferences (JSON, CSV, XLSX)
   - Timestamp configuration (format, include in filenames)
   - .env configuration options

2. **Generate project structure:**
   - `src/cli.py` — Main Click CLI entry point
   - `src/commands/{resource}_commands.py` — One file per API resource
   - `src/client.py` — HTTP client wrapper
   - `src/config.py` — Configuration management
   - `src/batch_processor.py` — Batch request processor
   - `.env.example` — Configuration template
   - `requirements.txt` — Dependencies
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

**References** — Configuration and specification guides for users of generated projects

No assets needed (all project files generated programmatically)
