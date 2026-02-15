# PRD: Tronscan API Python Client

**Version:** 1.0.0
**API Version:** 1.0.0
**Base URL:** https://apilist.tronscan.org
**License:** Apache 2.0
**Contact:** Tronscan Team (https://tronscan.org)

---

## Overview

The Tronscan API provides access to the TRON blockchain explorer, enabling developers to query accounts, transactions, blocks, smart contracts, tokens, and network statistics. This PRD defines best practices for building a Python client to interact with these endpoints efficiently.

**Key Features:**
- Query blockchain data (accounts, transactions, blocks)
- Retrieve smart contract and token information
- Access network statistics and parameters
- Paginated list endpoints for large datasets
- Read-only API (GET requests only)
- Free public access (no authentication required)

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- httpx >= 0.24.0
- pandas >= 1.5.0 (for CSV/XLSX output)
- openpyxl >= 3.0.0 (for XLSX support)

### Install Dependencies

```bash
pip install httpx pandas openpyxl
```

### Configuration

Create a `.env` file in your project root:

```env
# Tronscan API Configuration
TRONSCAN_BASE_URL=https://apilist.tronscan.org
TRONSCAN_API_KEY=your_api_key_here
TRONSCAN_TIMEOUT=30
TRONSCAN_RETRIES=3
TRONSCAN_RETRY_DELAY=1
TRONSCAN_LOG_LEVEL=INFO
```

Load configuration in your code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('TRONSCAN_BASE_URL', 'https://apilist.tronscan.org')
API_KEY = os.getenv('TRONSCAN_API_KEY')
TIMEOUT = int(os.getenv('TRONSCAN_TIMEOUT', 30))
MAX_RETRIES = int(os.getenv('TRONSCAN_RETRIES', 3))
INITIAL_RETRY_DELAY = float(os.getenv('TRONSCAN_RETRY_DELAY', 1))
```

---

## Authentication

Tronscan API requires an API key passed in the request header:

```python
import httpx

API_KEY = "your_api_key_here"

headers = {
    "X-API-Key": API_KEY,
    "User-Agent": "Tronscan-Python-Client/1.0"
}

async with httpx.AsyncClient(headers=headers, timeout=30) as client:
    response = await client.get(f"{BASE_URL}/api/account", params={"address": "..."})
```

### Getting an API Key

1. Visit https://tronscan.org
2. Register or log in
3. Navigate to API settings
4. Generate a new API key
5. Add to your `.env` file

---

## API Endpoints Reference

### ACCOUNTS

#### 1. Get Account Information

**Endpoint:** `GET /api/account`

**Purpose:** Retrieve detailed information about a TRON account by address.

**Python Example:**

```python
import httpx
import json

async def get_account(address: str):
    """Get account information by address."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/account",
            params={"address": address},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()

# Usage
import asyncio
account = asyncio.run(get_account("TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L"))
print(json.dumps(account, indent=2))
```

#### 2. Get Voting Information

**Endpoint:** `GET /api/account/{address}/votes`

**Purpose:** Retrieve voting information for a specific account.

**Python Example:**

```python
async def get_account_votes(address: str):
    """Get voting information for an account."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://apilist.tronscan.org/api/account/{address}/votes",
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()

# Usage
votes = asyncio.run(get_account_votes("TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L"))
```

#### 3. Get Paginated Account List

**Endpoint:** `GET /api/accountlist`

**Purpose:** Retrieve a paginated list of accounts.

**Query Parameters:**
- `start` (optional): Starting index
- `limit` (optional): Number of results per page (default: 20, max: 200)
- `sort` (optional): Sort field

**Python Example:**

```python
async def get_account_list(start: int = 0, limit: int = 20):
    """Get paginated list of accounts."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/accountlist",
            params={"start": start, "limit": limit},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

---

### TRANSACTIONS

#### 1. Get Transaction Details

**Endpoint:** `GET /api/transaction`

**Purpose:** Retrieve detailed information about a specific transaction by hash.

**Python Example:**

```python
async def get_transaction(tx_hash: str):
    """Get transaction details by hash."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/transaction",
            params={"hash": tx_hash},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Get Transaction Count

**Endpoint:** `GET /api/transaction/count`

**Purpose:** Get the total transaction count.

**Python Example:**

```python
async def get_transaction_count():
    """Get total transaction count."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/transaction/count",
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 3. Get Paginated Transaction List

**Endpoint:** `GET /api/transactionlist`

**Purpose:** Retrieve a paginated list of transactions.

**Parameters:**
- `start` (optional): Starting index
- `limit` (optional): Results per page
- `sort` (optional): Sort field

#### 4. Get Transaction Count Statistics

**Endpoint:** `GET /api/transactioncount`

**Purpose:** Get transaction count statistics.

---

### BLOCKS

#### 1. Get Block Information

**Endpoint:** `GET /api/block`

**Purpose:** Retrieve information about a block by number.

**Python Example:**

```python
async def get_block(block_number: int):
    """Get block information by number."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/block",
            params={"number": block_number},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Get Paginated Block List

**Endpoint:** `GET /api/blocklist`

**Purpose:** Retrieve a paginated list of blocks.

#### 3. Get Block Count

**Endpoint:** `GET /api/blockcount`

**Purpose:** Get the total block count.

---

### SMART CONTRACTS

#### 1. Get Smart Contract Information

**Endpoint:** `GET /api/contract`

**Purpose:** Retrieve information about a smart contract.

**Python Example:**

```python
async def get_contract(address: str):
    """Get smart contract information."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/contract",
            params={"address": address},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Get Paginated Contract List

**Endpoint:** `GET /api/contractlist`

**Purpose:** Retrieve a paginated list of smart contracts.

---

### TRANSFERS

#### 1. Get Token Transfer Information

**Endpoint:** `GET /api/transfer`

**Purpose:** Retrieve token transfer details.

**Python Example:**

```python
async def get_transfer(transfer_hash: str):
    """Get token transfer information."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/transfer",
            params={"hash": transfer_hash},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Get Paginated Transfer List

**Endpoint:** `GET /api/transferlist`

**Purpose:** Retrieve a paginated list of token transfers.

---

### TOKENS

#### 1. Get Token Information

**Endpoint:** `GET /api/token`

**Purpose:** Retrieve information about a token.

**Python Example:**

```python
async def get_token(address: str):
    """Get token information."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/token",
            params={"address": address},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Get Paginated Token List

**Endpoint:** `GET /api/tokenlist`

**Purpose:** Retrieve a paginated list of tokens.

---

### NETWORK

#### 1. Get Blockchain Network Parameters

**Endpoint:** `GET /api/chain/parameters`

**Purpose:** Retrieve blockchain network parameters and settings.

**Python Example:**

```python
async def get_chain_parameters():
    """Get blockchain network parameters."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/chain/parameters",
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Get Blockchain Statistics

**Endpoint:** `GET /api/chain/stat`

**Purpose:** Retrieve overall blockchain statistics.

**Python Example:**

```python
async def get_chain_stat():
    """Get blockchain statistics."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apilist.tronscan.org/api/chain/stat",
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
```

---

## Batch Request Processing

### CSV Batch Format

Create a CSV file with requests:

```csv
method,endpoint,address
GET,/api/account,TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L
GET,/api/account,TJzzWvwj8WJnhHa2H8QJgKvfAPXqnwXUHz
GET,/api/token,TR7NHqjeKQxGTCi8q282aCYGS1E9Fvqz9L
```

### Processing Batch Requests

```python
import csv
import asyncio
import httpx

async def process_batch_csv(csv_file: str):
    """Process batch requests from CSV file."""
    results = []

    async with httpx.AsyncClient(headers={"X-API-Key": API_KEY}) as client:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                method = row['method'].upper()
                endpoint = row['endpoint']

                try:
                    response = await client.request(
                        method,
                        f"https://apilist.tronscan.org{endpoint}",
                        params={k: v for k, v in row.items()
                               if k not in ['method', 'endpoint']},
                        timeout=30
                    )
                    response.raise_for_status()

                    results.append({
                        'endpoint': endpoint,
                        'status': 'success',
                        'data': response.json()
                    })
                except httpx.HTTPError as e:
                    results.append({
                        'endpoint': endpoint,
                        'status': 'error',
                        'error': str(e)
                    })

    return results

# Usage
results = asyncio.run(process_batch_csv('requests.csv'))
```

---

## Error Handling & Retry Logic

### HTTP Status Codes

- **200 OK:** Successful request
- **400 Bad Request:** Invalid parameters
- **401 Unauthorized:** Invalid or missing API key
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Resource not found
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Server Error:** Server-side error
- **502 Bad Gateway:** Temporary unavailability
- **503 Service Unavailable:** Maintenance or overload
- **504 Gateway Timeout:** Request timeout

### Retry Strategy

```python
import httpx
from typing import Optional
import time

async def request_with_retry(
    method: str,
    url: str,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_multiplier: float = 2.0
) -> Optional[dict]:
    """Execute request with exponential backoff retry logic."""

    retriable_status_codes = {408, 429, 500, 502, 503, 504}
    delay = initial_delay

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(
                headers={"X-API-Key": API_KEY},
                timeout=30
            ) as client:
                response = await client.request(method, url)

                if response.status_code in retriable_status_codes and attempt < max_retries - 1:
                    wait_time = delay * (0.9 + 0.2 * __import__('random').random())
                    print(f"Retry attempt {attempt + 1} after {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)
                    delay *= backoff_multiplier
                    continue

                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            if attempt == max_retries - 1:
                print(f"Max retries exceeded: {e}")
                return None

            wait_time = delay * (0.9 + 0.2 * __import__('random').random())
            await asyncio.sleep(wait_time)
            delay *= backoff_multiplier

    return None
```

---

## Output Formatting

### JSON Output

```python
import json

def format_json(data: dict) -> str:
    """Format response as JSON."""
    return json.dumps(data, indent=2)

# Save to file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### XLSX Output

```python
import pandas as pd

def export_to_xlsx(data: list, output_file: str):
    """Export results to Excel file."""
    df = pd.DataFrame(data)

    # Format floats with 0 decimal places
    float_cols = df.select_dtypes(include=['float64']).columns
    df[float_cols] = df[float_cols].astype('int64')

    # Save without index
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Data exported to {output_file}")

# Usage
results = [
    {'address': 'TR7NHq...', 'balance': '1000000000'},
    {'address': 'TJzzWv...', 'balance': '500000000'}
]
export_to_xlsx(results, 'accounts.xlsx')
```

---

## Performance Optimization

### Connection Pooling

```python
import httpx

# Reuse client for multiple requests
async def query_multiple_accounts(addresses: list):
    """Query multiple accounts efficiently with connection pooling."""

    limits = httpx.Limits(max_connections=10, max_keepalive_connections=10)

    async with httpx.AsyncClient(
        limits=limits,
        headers={"X-API-Key": API_KEY},
        timeout=30
    ) as client:
        tasks = [
            client.get(
                "https://apilist.tronscan.org/api/account",
                params={"address": addr}
            )
            for addr in addresses
        ]

        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

### Rate Limiting

```python
import asyncio
from typing import List

async def rate_limited_requests(
    urls: List[str],
    requests_per_second: float = 2.0
):
    """Execute requests with rate limiting (100ms delay between requests)."""

    delay = 1.0 / requests_per_second

    async with httpx.AsyncClient(
        headers={"X-API-Key": API_KEY}
    ) as client:
        for url in urls:
            response = await client.get(url)
            yield response.json()
            await asyncio.sleep(delay)
```

### Pagination Pattern

```python
async def fetch_all_pages(endpoint: str, limit: int = 200):
    """Fetch all pages of paginated endpoint."""
    all_results = []
    start = 0

    async with httpx.AsyncClient(
        headers={"X-API-Key": API_KEY}
    ) as client:
        while True:
            response = await client.get(
                f"https://apilist.tronscan.org{endpoint}",
                params={"start": start, "limit": limit}
            )
            response.raise_for_status()

            data = response.json()
            if not data.get('data'):
                break

            all_results.extend(data['data'])
            start += limit

    return all_results
```

---

## Logging Best Practices

### Configure Logging

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tronscan_client.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_request(method: str, url: str, params: dict = None):
    """Log API request."""
    logger.info(f"Request: {method} {url} with params={params}")

def log_response(status_code: int, response_time: float):
    """Log API response."""
    logger.info(f"Response: Status={status_code}, Duration={response_time:.2f}s")

def log_error(error: Exception, retry_attempt: int = 0):
    """Log errors with retry context."""
    if retry_attempt > 0:
        logger.warning(f"Retry attempt {retry_attempt}: {error}")
    else:
        logger.error(f"Error: {error}")
```

### Debug Mode

```python
def enable_debug_logging():
    """Enable detailed debug logging."""
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('httpx').setLevel(logging.DEBUG)

    logger.debug("Debug logging enabled")
    logger.debug(f"API Key: {API_KEY[:10]}...")
    logger.debug(f"Base URL: {BASE_URL}")
```

---

## Best Practices Summary

1. **Always use API keys securely** - Never hardcode keys, use environment variables
2. **Implement exponential backoff** - Use jittered delays to avoid thundering herd
3. **Handle rate limits gracefully** - Respect 429 responses and adjust request rate
4. **Use connection pooling** - Reuse httpx clients for efficiency
5. **Log all requests** - Track API usage for debugging and auditing
6. **Cache when appropriate** - Store frequently accessed data locally
7. **Validate parameters** - Check inputs before sending requests
8. **Use timeouts** - Always set request timeouts to prevent hanging
9. **Process batches efficiently** - Use async for concurrent requests
10. **Monitor quota usage** - Track API calls against any limits

---

## Troubleshooting

### Common Errors

**401 Unauthorized**
- Verify API key in `.env` file
- Check header format: `X-API-Key: your_key_here`
- Ensure API key hasn't expired

**429 Too Many Requests**
- Implement exponential backoff retry logic
- Add rate limiting (100ms+ between requests)
- Check if quota has been exceeded

**504 Gateway Timeout**
- Increase timeout value in client configuration
- Reduce batch size for concurrent requests
- Implement retry logic with longer delays

**Empty Response**
- Verify endpoint URL and parameters
- Check if resource exists (404 errors)
- Ensure required parameters are provided

---

## Related Resources

- **API Documentation:** https://tronscan.org
- **TRON Network:** https://tron.network
- **httpx Documentation:** https://www.python-httpx.org
- **Pandas Documentation:** https://pandas.pydata.org

---

**Last Updated:** 2026-02-15
**Status:** Ready for Python CLI development
