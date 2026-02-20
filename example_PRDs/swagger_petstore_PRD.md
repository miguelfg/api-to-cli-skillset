# PRD: Swagger Petstore Python API Client

**API Version:** 1.0.7
**Base URL:** `https://petstore.swagger.io/v2`
**Contact:** apiteam@swagger.io
**Documentation:** http://swagger.io

---

## Overview

The Petstore API provides endpoints for managing pets, orders, and users in a pet store system. This PRD documents a Python HTTP client library built with the `requests` library, designed for easy integration into Python applications.

**Supported Resources:**
- **Pets** — CRUD operations, search by status/tags, image uploads
- **Orders** — Place, retrieve, and cancel pet orders
- **Users** — User management, authentication, login/logout

---

## Installation

### Prerequisites
- Python 3.7+
- `pip` package manager

### Setup

```bash
# Install the package
pip install petstore-api-client

# Or install from source with development dependencies
git clone <repo-url>
cd petstore-client
pip install -e ".[dev]"
```

### Dependencies

The client requires:
```
requests>=2.28.0          # HTTP client with connection pooling
pandas>=1.3.0             # Data manipulation and export (CSV/XLSX)
click>=8.0.0              # CLI framework
pydantic>=1.10.0          # Data validation
python-dotenv>=0.19.0     # Environment variable management
openpyxl>=3.7.0           # XLSX support
```

---

## Authentication

The Petstore API uses **API Key** authentication via HTTP header.

### Obtaining an API Key

For this sample API, use the test key:
```
API_KEY=special-key
```

### Setting Up Authentication

**Option 1: Environment Variable**
```bash
export PETSTORE_API_KEY="special-key"
```

**Option 2: .env File**
```bash
# Create .petstore_settings.json in your project directory
cat > .petstore_settings.json << EOF
{
  "api_key": "special-key",
  "base_url": "https://petstore.swagger.io/v2",
  "timeout": 30,
  "retry_count": 3,
  "cache_enabled": true,
  "log_level": "INFO"
}
EOF
```

**Option 3: Direct Configuration**
```python
from petstore_client import PetstoreClient

client = PetstoreClient(api_key="special-key")
```

---

## Quick Start

### Using the Python Client

```python
from petstore_client import PetstoreClient

# Initialize client
client = PetstoreClient(api_key="special-key")

# Fetch a pet by ID
pet = client.get_pet(pet_id=1)
print(pet)

# List all available pets
available_pets = client.find_pets_by_status(status=["available"])
print(f"Found {len(available_pets)} available pets")

# Create a new pet
new_pet = client.add_pet(
    name="Fluffy",
    photo_urls=["https://example.com/fluffy.jpg"],
    status="available"
)
print(f"Created pet with ID: {new_pet['id']}")
```

### Using the CLI

```bash
# List available pets
petstore-cli pets list --status available

# Get pet details
petstore-cli pets get 1

# Create a pet
petstore-cli pets create --name "Buddy" --status "available"

# Export to CSV
petstore-cli pets list --status available --format csv --output pets.csv

# Export to Excel
petstore-cli pets list --format xlsx --output pets.xlsx
```

---

## API Endpoints

### PETS Resource

#### 1. Add Pet to Store
**Endpoint:** `POST /pet`
**Summary:** Add a new pet to the store

```python
# Python: requests library
import requests
import json

headers = {"api_key": "special-key"}
data = {
    "name": "Fluffy",
    "photoUrls": ["https://example.com/fluffy.jpg"],
    "status": "available",
    "tags": [{"name": "cute"}]
}

response = requests.post(
    "https://petstore.swagger.io/v2/pet",
    headers=headers,
    json=data,
    timeout=30
)
pet = response.json()
```

```bash
# CLI
petstore-cli pets create \
  --name "Fluffy" \
  --photo-urls "https://example.com/fluffy.jpg" \
  --status "available"
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Pet name |
| photoUrls | array | Yes | List of photo URLs |
| status | string | No | Pet status (available, pending, sold) |
| tags | array | No | List of tags |

**Response:** Pet object with assigned `id`

---

#### 2. Get Pet by ID
**Endpoint:** `GET /pet/{petId}`
**Summary:** Get a pet by its ID

```python
response = requests.get(
    f"https://petstore.swagger.io/v2/pet/{pet_id}",
    headers={"api_key": "special-key"},
    timeout=30
)
pet = response.json()
print(f"Pet: {pet['name']}, Status: {pet['status']}")
```

```bash
# CLI
petstore-cli pets get 1
petstore-cli pets get 1 --format json
```

**Parameters:**
| Name | Type | Location | Required |
|------|------|----------|----------|
| petId | integer | path | Yes |

**Response:** Pet object

---

#### 3. Find Pets by Status
**Endpoint:** `GET /pet/findByStatus`
**Summary:** Find pets by status

```python
import requests

response = requests.get(
    "https://petstore.swagger.io/v2/pet/findByStatus",
    headers={"api_key": "special-key"},
    params={"status": ["available", "pending"]},
    timeout=30
)
pets = response.json()
print(f"Found {len(pets)} pets")

# Export to pandas DataFrame
import pandas as pd
df = pd.DataFrame(pets)
df.to_csv("pets.csv", index=False)  # Save to CSV
```

```bash
# CLI
petstore-cli pets list --status available
petstore-cli pets list --status available --status pending
petstore-cli pets list --status available --format csv --output pets.csv
petstore-cli pets list --status available --format xlsx --output pets.xlsx
```

**Parameters:**
| Name | Type | Location | Required | Values |
|------|------|----------|----------|--------|
| status | array | query | Yes | available, pending, sold |

**Response:** Array of Pet objects

---

#### 4. Update Pet
**Endpoint:** `PUT /pet`
**Summary:** Update an existing pet

```python
data = {
    "id": 1,
    "name": "Fluffier",
    "status": "sold"
}

response = requests.put(
    "https://petstore.swagger.io/v2/pet",
    headers={"api_key": "special-key"},
    json=data,
    timeout=30
)
updated_pet = response.json()
```

```bash
# CLI
petstore-cli pets update --id 1 --name "Fluffier" --status "sold"
```

---

#### 5. Delete Pet
**Endpoint:** `DELETE /pet/{petId}`
**Summary:** Delete a pet

```python
response = requests.delete(
    f"https://petstore.swagger.io/v2/pet/{pet_id}",
    headers={"api_key": "special-key"},
    timeout=30
)
```

```bash
# CLI
petstore-cli pets delete 1
```

---

### ORDERS Resource

#### 1. Place Order
**Endpoint:** `POST /store/order`
**Summary:** Place an order for a pet

```python
data = {
    "petId": 1,
    "quantity": 2,
    "shipDate": "2026-02-15T12:00:00Z",
    "status": "placed",
    "complete": False
}

response = requests.post(
    "https://petstore.swagger.io/v2/store/order",
    json=data,
    timeout=30
)
order = response.json()
print(f"Order ID: {order['id']}")
```

```bash
# CLI
petstore-cli orders create \
  --pet-id 1 \
  --quantity 2 \
  --status "placed"
```

---

#### 2. Get Order by ID
**Endpoint:** `GET /store/order/{orderId}`
**Summary:** Get an order by ID

```python
response = requests.get(
    f"https://petstore.swagger.io/v2/store/order/{order_id}",
    timeout=30
)
order = response.json()
```

```bash
# CLI
petstore-cli orders get 1
petstore-cli orders get 1 --format csv
```

---

#### 3. Delete Order
**Endpoint:** `DELETE /store/order/{orderId}`
**Summary:** Delete an order

```python
response = requests.delete(
    f"https://petstore.swagger.io/v2/store/order/{order_id}",
    timeout=30
)
```

```bash
# CLI
petstore-cli orders delete 1
```

---

### USERS Resource

#### 1. Create User
**Endpoint:** `POST /user`
**Summary:** Create a new user

```python
data = {
    "username": "john_doe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "password": "secret123",
    "phone": "555-1234"
}

response = requests.post(
    "https://petstore.swagger.io/v2/user",
    headers={"api_key": "special-key"},
    json=data,
    timeout=30
)
```

```bash
# CLI
petstore-cli users create \
  --username "john_doe" \
  --first-name "John" \
  --last-name "Doe" \
  --email "john@example.com"
```

---

#### 2. Get User by Username
**Endpoint:** `GET /user/{username}`
**Summary:** Get user by username

```python
response = requests.get(
    f"https://petstore.swagger.io/v2/user/{username}",
    headers={"api_key": "special-key"},
    timeout=30
)
user = response.json()
```

```bash
# CLI
petstore-cli users get john_doe
petstore-cli users get john_doe --format json
```

---

#### 3. Update User
**Endpoint:** `PUT /user/{username}`
**Summary:** Update user information

```python
data = {
    "email": "john.doe@example.com",
    "phone": "555-5678"
}

response = requests.put(
    f"https://petstore.swagger.io/v2/user/{username}",
    headers={"api_key": "special-key"},
    json=data,
    timeout=30
)
```

```bash
# CLI
petstore-cli users update john_doe --email "john.doe@example.com"
```

---

#### 4. Delete User
**Endpoint:** `DELETE /user/{username}`
**Summary:** Delete a user

```python
response = requests.delete(
    f"https://petstore.swagger.io/v2/user/{username}",
    headers={"api_key": "special-key"},
    timeout=30
)
```

```bash
# CLI
petstore-cli users delete john_doe
```

---

#### 5. Login User
**Endpoint:** `GET /user/login`
**Summary:** Authenticate a user

```python
response = requests.get(
    "https://petstore.swagger.io/v2/user/login",
    headers={"api_key": "special-key"},
    params={"username": "john_doe", "password": "secret123"},
    timeout=30
)
auth_token = response.json()
print(f"Token: {auth_token}")
```

```bash
# CLI
petstore-cli users login --username john_doe --password secret123
```

---

## Error Handling

The client implements robust error handling with automatic retry logic for transient failures.

### Error Classification

**1. Network Errors (Retriable)**
- Connection timeouts
- HTTP 5xx errors (500, 502, 503, 504)
- Rate limit errors (HTTP 429)
- Request timeout (HTTP 408)

**Action:** Retry with exponential backoff

```python
from petstore_client import PetstoreClient, NetworkError

try:
    client = PetstoreClient(api_key="special-key")
    pet = client.get_pet(pet_id=1)
except NetworkError as e:
    print(f"Network error (retried 3 times): {e}")
    # Implement fallback logic
```

**2. Client Errors (Non-Retriable)**
- Invalid parameters (HTTP 400)
- Not found (HTTP 404)
- Invalid API key (HTTP 401)
- Forbidden (HTTP 403)

**Action:** Display error message, do not retry

```python
from petstore_client import ClientError

try:
    pet = client.get_pet(pet_id=99999)
except ClientError as e:
    print(f"Client error: {e.status_code} - {e.message}")
    # Handle specific error
```

**3. Data Errors (Validation Failures)**
- Invalid JSON response
- Schema validation failures

**Action:** Raise exception with details

```python
from petstore_client import DataError

try:
    pet = client.get_pet(pet_id=1)
except DataError as e:
    print(f"Data validation error: {e}")
```

### Retry Logic with Exponential Backoff

**Default Configuration:**
- **Max attempts:** 3
- **Initial delay:** 1 second
- **Backoff multiplier:** 2 (1s → 2s → 4s)
- **Jitter:** ±10% randomization
- **Retriable status codes:** 408, 429, 500, 502, 503, 504

```python
# Example: Automatic retry with backoff
client = PetstoreClient(
    api_key="special-key",
    retry_count=3,
    initial_delay=1.0,
    backoff_multiplier=2.0,
    jitter=0.1
)

# This will automatically retry on 5xx or 429 errors
pets = client.find_pets_by_status(status=["available"])
```

**Custom Retry Configuration:**

```python
client = PetstoreClient(
    api_key="special-key",
    retry_count=5,          # More retries
    initial_delay=0.5,      # Shorter initial delay
    backoff_multiplier=1.5  # Gentler backoff
)
```

---

## Connection Pooling

The client uses connection pooling to optimize performance and reduce overhead.

### Configuration

**Default Settings:**
- **Pool size:** 10 connections
- **Timeout:** 30 seconds per request
- **Connection keep-alive:** Enabled

```python
from requests.adapters import HTTPAdapter

client = PetstoreClient(api_key="special-key")

# Pre-configured with optimal pooling
# Uses: requests.Session with HTTPAdapter
#   - pool_connections=10
#   - pool_maxsize=10
#   - max_retries with backoff strategy
```

### Performance Benefits

```python
import time
from petstore_client import PetstoreClient

client = PetstoreClient(api_key="special-key")

# First request: ~500ms (new connection)
start = time.time()
pet1 = client.get_pet(pet_id=1)
print(f"First request: {(time.time() - start)*1000:.0f}ms")

# Second request: ~50ms (connection reused from pool)
start = time.time()
pet2 = client.get_pet(pet_id=2)
print(f"Second request: {(time.time() - start)*1000:.0f}ms")
```

---

## Caching Strategy

The client includes intelligent caching to reduce API calls and improve performance.

### Cache Behavior

**Cached Operations:** GET requests (read-only operations)
**Cache Duration:** 5 minutes (configurable)
**Cache Key:** Hash of endpoint + parameters
**Storage:** In-memory (default) or file-based

```python
client = PetstoreClient(
    api_key="special-key",
    cache_enabled=True,      # Enable caching
    cache_ttl=300            # 5 minutes
)

# First call: Hits API, caches result
pets1 = client.find_pets_by_status(status=["available"])
# ~500ms

# Second call (within 5 min): Returns cached result
pets2 = client.find_pets_by_status(status=["available"])
# ~1ms

# Bypass cache with override flag
pets3 = client.find_pets_by_status(status=["available"], use_cache=False)
# ~500ms (fresh from API)
```

### Cache Management

The CLI includes cache management commands:

```bash
# List cached entries
petstore-cli cache list

# Show cache statistics
petstore-cli cache info

# Clear all cache
petstore-cli cache clear

# Clear specific cache entry
petstore-cli cache delete "get_pet:1"

# Clear cache for specific resource
petstore-cli cache clear --resource pets
```

### Disabling Cache

```python
# Disable caching globally
client = PetstoreClient(api_key="special-key", cache_enabled=False)

# Or disable per-request
pet = client.get_pet(pet_id=1, use_cache=False)
```

---

## Configuration Management

Settings are stored in `.petstore_settings.json` in your project directory.

### Default Configuration

```json
{
  "api_key": "special-key",
  "base_url": "https://petstore.swagger.io/v2",
  "timeout": 30,
  "retry_count": 3,
  "initial_delay": 1.0,
  "backoff_multiplier": 2.0,
  "jitter": 0.1,
  "cache_enabled": true,
  "cache_ttl": 300,
  "log_level": "INFO",
  "api_delay": 0.1
}
```

### Loading Configuration

**Option 1: Automatic (from file)**
```python
from petstore_client import load_config

client = PetstoreClient.from_config()  # Reads .petstore_settings.json
```

**Option 2: Manual**
```python
import json
from petstore_client import PetstoreClient

with open(".petstore_settings.json") as f:
    config = json.load(f)

client = PetstoreClient(**config)
```

### CLI Configuration Commands

```bash
# Show current configuration
petstore-cli config show

# Update a setting
petstore-cli config set api_key "new-key"
petstore-cli config set cache_ttl 600

# Reset to defaults
petstore-cli config reset

# View config file location
petstore-cli config path
```

---

## Logging

The client logs all API interactions for debugging and auditing.

### Log Levels

- **DEBUG:** Full request/response payloads, stack traces
- **INFO:** Operation summaries, cache hits, request duration
- **WARNING:** Retry attempts, rate limiting, deprecated endpoints
- **ERROR:** Failed requests, validation errors

### Configuration

```python
import logging
from petstore_client import PetstoreClient

# Set log level
logging.basicConfig(level=logging.INFO)

client = PetstoreClient(
    api_key="special-key",
    log_level="INFO"  # Or DEBUG, WARNING, ERROR
)
```

### Example Logs

```
[INFO] 2026-02-15 10:30:45 - GET /pet/findByStatus [cached=false] (245ms)
[INFO] 2026-02-15 10:30:46 - POST /pet [201] (320ms) Created pet: Fluffy
[WARNING] 2026-02-15 10:30:47 - Rate limit detected, backing off (429)
[DEBUG] 2026-02-15 10:30:48 - Request: POST /user, Headers: {'api_key': '***'}
[ERROR] 2026-02-15 10:30:49 - Failed to get pet (max retries exceeded)
```

### Debug Mode (Verbose)

Enable with CLI flag:

```bash
# Show full request/response details
petstore-cli pets list --verbose

# Output:
# [DEBUG] Request: GET /pet/findByStatus?status=available
# [DEBUG] Headers: {'api-key': '***', 'User-Agent': 'petstore-client/1.0'}
# [DEBUG] Response: 200 OK
# [DEBUG] Body: [{"id": 1, "name": "Fluffy", ...}, ...]
```

---

## Output Formats

The client supports multiple output formats for different use cases.

### Format Types

#### JSON (Default)
```bash
petstore-cli pets list --status available --format json
```

**Output:**
```json
[
  {
    "id": 1,
    "name": "Fluffy",
    "photoUrls": ["https://example.com/fluffy.jpg"],
    "status": "available",
    "tags": []
  }
]
```

**Use case:** Scripting, piping to `jq`, structured data processing

#### CSV
```bash
petstore-cli pets list --status available --format csv
```

**Output:**
```
id,name,photoUrls,status,tags
1,Fluffy,"['https://example.com/fluffy.jpg']",available,[]
2,Buddy,"['https://example.com/buddy.jpg']",available,[]
```

**Formatting:**
- UTF-8 encoding by default
- Floats formatted with 0 decimal places
- Index column excluded

**Export to file:**
```bash
petstore-cli pets list --format csv --output pets.csv
```

#### XLSX (Excel)
```bash
petstore-cli pets list --status available --format xlsx --output pets.xlsx
```

**Features:**
- Column headers with bold formatting
- Auto-sized columns
- Data types preserved (dates, numbers)
- Multiple sheets support (resource groups)

**Use case:** Data analysis, sharing with non-technical users, Excel workflows

#### Python Usage

```python
import pandas as pd
from petstore_client import PetstoreClient

client = PetstoreClient(api_key="special-key")

# Get data as dict (default)
pets = client.find_pets_by_status(status=["available"])

# Convert to pandas DataFrame for export
df = pd.DataFrame(pets)

# Export to CSV
df.to_csv("pets.csv", index=False, encoding="utf-8")

# Export to Excel
df.to_excel("pets.xlsx", index=False)
```

---

## CLI Structure

The CLI is organized using Click command groups for logical operation hierarchies.

### Command Structure

```
petstore-cli
├── pets (subgroup)
│   ├── list      -- Find pets by status
│   ├── get       -- Get pet by ID
│   ├── create    -- Add new pet
│   ├── update    -- Update pet
│   └── delete    -- Delete pet
├── orders (subgroup)
│   ├── list      -- List orders
│   ├── get       -- Get order by ID
│   ├── create    -- Place order
│   └── delete    -- Delete order
├── users (subgroup)
│   ├── list      -- List users
│   ├── get       -- Get user by username
│   ├── create    -- Create user
│   ├── update    -- Update user
│   ├── delete    -- Delete user
│   └── login     -- Authenticate user
├── cache (subgroup)
│   ├── list      -- Show cached entries
│   ├── info      -- Cache statistics
│   ├── clear     -- Clear cache
│   └── delete    -- Delete specific cache entry
└── config (subgroup)
    ├── show      -- Show current settings
    ├── set       -- Update setting
    ├── reset     -- Reset to defaults
    └── path      -- Show config file location
```

### Usage Examples

```bash
# Pets commands
petstore-cli pets list --status available --format csv --output pets.csv
petstore-cli pets get 1
petstore-cli pets create --name "Buddy" --status "available"
petstore-cli pets update --id 1 --status "sold"
petstore-cli pets delete 1

# Orders commands
petstore-cli orders list
petstore-cli orders get 5
petstore-cli orders create --pet-id 1 --quantity 2
petstore-cli orders delete 5

# Users commands
petstore-cli users list
petstore-cli users get john_doe
petstore-cli users create --username "alice" --email "alice@example.com"
petstore-cli users update alice --email "alice.new@example.com"
petstore-cli users delete alice
petstore-cli users login --username john_doe --password secret123

# Cache management
petstore-cli cache list
petstore-cli cache info
petstore-cli cache clear
petstore-cli cache delete "find_pets:available"

# Configuration
petstore-cli config show
petstore-cli config set cache_ttl 600
petstore-cli config reset
```

### Common Flags

**All commands support:**
```bash
--help              # Show command help
--verbose           # Enable debug logging
--format json|csv|xlsx  # Output format
--output FILE       # Save to file
--dry-run           # Simulate without executing
```

**List commands support:**
```bash
--skip N            # Skip first N records (pagination)
--limit N           # Limit to N records (pagination)
--override          # Bypass cache, fetch fresh
```

---

## Best Practices

### 1. Use Context Managers for Error Handling

```python
from petstore_client import PetstoreClient
from petstore_client.exceptions import PetstoreError

try:
    client = PetstoreClient(api_key="special-key")
    pet = client.get_pet(pet_id=1)
    print(f"Pet: {pet['name']}")
except PetstoreError as e:
    logger.error(f"Failed to fetch pet: {e}")
    # Implement fallback
```

### 2. Batch Operations Efficiently

```python
# Good: Reuse session
client = PetstoreClient(api_key="special-key")
for pet_id in range(1, 100):
    pet = client.get_pet(pet_id)
    process(pet)

# Avoid: Creating new client for each request
for pet_id in range(1, 100):
    client = PetstoreClient(api_key="special-key")  # New session each time
    pet = client.get_pet(pet_id)
```

### 3. Cache Management

```python
# Clear cache before fetching fresh data
client.cache.clear()
pets = client.find_pets_by_status(status=["available"])

# Or bypass cache per-request
pets = client.find_pets_by_status(status=["available"], use_cache=False)
```

### 4. Logging and Debugging

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

client = PetstoreClient(api_key="special-key", log_level="DEBUG")
```

### 5. API Courtesy

The client includes built-in API courtesy practices:

```python
client = PetstoreClient(
    api_key="special-key",
    api_delay=0.1  # 100ms delay between requests
)

# Respects rate limit headers (X-RateLimit-*)
# Implements exponential backoff on 429 responses
# Caches GET requests to minimize redundant calls
```

### 6. Data Export Pipeline

```python
import pandas as pd
from petstore_client import PetstoreClient

client = PetstoreClient(api_key="special-key")

# Fetch data
pets = client.find_pets_by_status(status=["available"])

# Convert to DataFrame
df = pd.DataFrame(pets)

# Clean and transform
df['name'] = df['name'].str.title()
df = df[['id', 'name', 'status']]

# Export
df.to_csv("available_pets.csv", index=False, encoding="utf-8")
df.to_excel("available_pets.xlsx", index=False)
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid API key | Check `api_key` in config |
| `429 Too Many Requests` | Rate limited | Client auto-retries; check `api_delay` setting |
| `Connection Timeout` | Network issue | Increase `timeout` in config; check network |
| `Cache returning stale data` | Cache TTL too high | Use `--override` flag or lower `cache_ttl` |
| `Command not found` | CLI not installed | Run `pip install -e .` from project directory |
| `ModuleNotFoundError: requests` | Missing dependency | Run `pip install -r requirements.txt` |

---

## References

- **API Docs:** http://swagger.io
- **Requests Library:** https://requests.readthedocs.io/
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Click Framework:** https://click.palletsprojects.com/

---

**Generated:** 2026-02-15
**API Version:** 1.0.7
**Client Version:** 1.0.0
