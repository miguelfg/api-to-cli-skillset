# Generated Project Structure

When you run the skill, it generates a complete Python Click CLI project with the following structure:

## Full Directory Layout

```
my_api_client/
├── src/
│   ├── __init__.py
│   ├── cli.py                 # Main CLI entry point
│   ├── client.py              # HTTP client library
│   ├── config.py              # Configuration management
│   ├── batch_processor.py      # Batch request processor
│   └── commands/
│       ├── __init__.py
│       ├── pets_commands.py    # One file per API resource
│       ├── orders_commands.py
│       └── users_commands.py
├── data/                      # Input batch files (user-provided)
│   ├── pets-batch.csv
│   ├── orders-batch.txt
│   └── users-batch.csv
├── output/                    # Batch processing results (auto-created)
│   ├── results_20260215_143022.json
│   └── results_20260215_143523.xlsx
├── .env                       # Configuration (copy from .env.example)
├── .env.example              # Configuration template
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation (from assets/README_template.md)
```

---

## File Descriptions

### `src/cli.py` — Main CLI Entry Point
**Purpose:** Root Click group that registers all resource commands

**Key Features:**
- Global options: `--config`, `--verbose`
- Subcommands for each API resource (pets, orders, users)
- Batch processing command for bulk requests
- Configuration loading and initialization

**Usage:**
```bash
python -m src.cli --help
python -m src.cli pets --help
python -m src.cli batch --help
```

---

### `src/client.py` — HTTP Client Library
**Purpose:** Wrapper around requests library for API calls

**Functionality:**
- Authentication setup (API Key, Bearer Token)
- HTTP methods: GET, POST, PUT, DELETE
- Error handling and response parsing
- Session management with connection pooling

**Usage:**
```python
from src.client import APIClient
from src.config import Config

client = APIClient(Config())
pets = client.get('/pet/findByStatus', {'status': 'available'})
```

---

### `src/config.py` — Configuration Management
**Purpose:** Load and manage settings from `.env` file

**Functionality:**
- Load environment variables from `.env`
- Get/set configuration values
- Save configuration changes
- Defaults and fallbacks

**Usage:**
```python
from src.config import Config

config = Config()
api_key = config.get('api_key')
config.set('log_level', 'DEBUG')
config.save()
```

---

### `src/batch_processor.py` — Batch Request Processor
**Purpose:** Process bulk requests from CSV/TXT files

**Functionality:**
- Parse CSV and TXT (JSON Lines) formats
- Execute requests sequentially
- Save results in JSON/CSV/XLSX format
- Support timestamp in filenames
- Error handling and logging

**Usage:**
```bash
python -m src.cli batch \
  --input-file data/pets-batch.csv \
  --format json \
  --output-path ./output \
  --include-timestamp
```

---

### `src/commands/{resource}_commands.py` — Resource Commands
**One file per API resource** (e.g., `pets_commands.py`, `users_commands.py`)

**Generated Commands per Resource:**
- `list` — List all resources
- `get` — Get specific resource by ID
- `create` — Create new resource
- `update` — Update existing resource (if applicable)
- `delete` — Delete resource (if applicable)

**Structure:**
```python
@click.group()
def pets_group():
    """Manage pets resources."""
    pass

@pets_group.command()
def list():
    """List all pets."""
    pass

@pets_group.command()
def get():
    """Get pet by ID."""
    pass
```

---

### `.env` — Configuration File
**Purpose:** Store sensitive configuration and settings

**Contents:**
```env
# API Connection
base_url=https://petstore.swagger.io/v2
api_key=your_api_key
api_token=your_bearer_token

# Output Configuration
output_format=json
timestamp_format=%Y%m%d_%H%M%S
include_timestamp=false

# Batch Processing
batch_input_format=csv
batch_output_path=./output

# Logging
log_level=INFO
verbose=false
```

**Note:** Always copy from `.env.example` and customize!

---

### `requirements.txt` — Python Dependencies
**Contents:**
```
click>=8.0.0
requests>=2.28.0
python-dotenv>=0.19.0
pandas>=1.3.0
openpyxl>=3.7.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

### `README.md` — Project Documentation

**Purpose:** Quick-start guide for users of the generated CLI project.

Generated from `assets/README_template.md` in the `prd-to-cli` skill, with placeholders
replaced by values extracted from the PRD:

| Placeholder | Replaced with |
|-------------|--------------|
| `[PROJECT_NAME]` | Project name (e.g., `tronscan-cli`) |
| `[API_NAME]` | API name from PRD title |
| `[CLI_NAME]` | CLI command name (e.g., `tronscan`) |
| `[API_PREFIX]` | Env var prefix (e.g., `TRONSCAN`) |
| `[BASE_URL]` | Base URL from PRD |
| `[AUTH_HEADER]` | Auth header name (e.g., `TRON-PRO-API-KEY`) |
| `[RESOURCE_LIST]` | Bullet list of resources and their commands |
| `[RESOURCE_COMMAND_EXAMPLES]` | Example CLI commands per resource |
| `[BATCH_EXAMPLES]` | Sample batch `.txt` entries |
| `[COMMAND_FILES]` | List of `src/commands/*.py` files |
| `[PRD_PATH]` | Relative path to the source PRD.md |

---

## Resource Commands Organization

Each API resource from the PRD becomes a Click command group with subcommands:

### Example: Pets Resource
```bash
# List all pets
python -m src.cli pets list

# Get pet by ID
python -m src.cli pets get --id 1

# Create new pet
python -m src.cli pets create --data '{"name": "Fluffy"}'

# Update pet
python -m src.cli pets update --id 1 --data '{"status": "sold"}'

# Delete pet
python -m src.cli pets delete --id 1
```

### Generated File: `src/commands/pets_commands.py`
```python
@click.group()
def pets_group(ctx):
    """Manage pets resources."""
    ctx.obj = ctx.obj or {}

@pets_group.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'xlsx']), default='json')
def list(format):
    """List all pets."""
    # Implementation

@pets_group.command()
@click.argument('id')
def get(id):
    """Get a pet by ID."""
    # Implementation

@pets_group.command()
@click.option('--data', type=str, help='JSON data')
def create(data):
    """Create a new pet."""
    # Implementation
```

---

## Data Directory

**Location:** `data/`
**Purpose:** Store input batch files (user-created)

**File Types:**
- `*.csv` — CSV format batch requests
- `*.txt` — JSON Lines format batch requests

**Example:** `data/pets-batch.csv`
```csv
method,endpoint,name,status
GET,/pet/findByStatus,available
POST,/pet,Fluffy,available
GET,/pet/1
```

---

## Output Directory

**Location:** `output/`
**Purpose:** Store batch processing results (auto-created)

**Generated Files:**
- `results.json` — Default results format
- `results_20260215_143022.json` — With timestamp
- `results.csv` — CSV export
- `results.xlsx` — Excel export

**Example:** `output/results.json`
```json
[
  {
    "method": "GET",
    "endpoint": "/pet/1",
    "status": 200,
    "data": {"id": 1, "name": "Fluffy"}
  }
]
```

---

## How Resources Map from PRD

The skill extracts API resources from your PRD.md based on section headers:

**PRD.md:**
```markdown
### PETS Resource
#### 1. List Pets
#### 2. Get Pet by ID
...

### ORDERS Resource
#### 1. Place Order
...

### USERS Resource
#### 1. Create User
...
```

**Generated Files:**
```
src/commands/pets_commands.py
src/commands/orders_commands.py
src/commands/users_commands.py
```

**CLI Structure:**
```
python -m src.cli pets list
python -m src.cli orders create
python -m src.cli users get
```

---

## Customization Points

After generation, you can customize:

1. **Add new commands** — Edit `src/commands/{resource}_commands.py`
2. **Enhance client** — Add methods to `src/client.py`
3. **Update config** — Modify `.env` settings
4. **Change defaults** — Edit `src/config.py` defaults
5. **Add validation** — Enhance parameter handling in commands

---

## Quick Start After Generation

```bash
# 1. Navigate to project
cd my_api_client

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API
cp .env.example .env
# Edit .env with your API key and settings

# 4. Test a command
python -m src.cli pets list

# 5. Process batch file
python -m src.cli batch \
  --input-file data/pets-batch.csv \
  --format json \
  --output-path output
```
