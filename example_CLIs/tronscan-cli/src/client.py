"""HTTP client for Tronscan API with retry logic and connection pooling."""

import asyncio
import logging
import random
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)


class TronscanClient:
    """Async HTTP client for Tronscan API with built-in retry logic."""

    RETRIABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize Tronscan API client."""
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        skip_retry: bool = False,
    ) -> Dict[str, Any]:
        """Execute GET request with optional retry logic."""
        url = f"{self.base_url}{endpoint}"
        headers = {"User-Agent": "Tronscan-Python-CLI/1.0"}

        if self.api_key:
            headers["X-API-Key"] = self.api_key

        if skip_retry:
            return await self._execute_request("GET", url, params, headers)

        return await self._execute_with_retry("GET", url, params, headers)

    async def _execute_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Execute single request."""
        limits = httpx.Limits(max_connections=10, max_keepalive_connections=10)

        async with httpx.AsyncClient(
            limits=limits,
            timeout=self.timeout,
            headers=headers,
        ) as client:
            response = await client.request(method, url, params=params)
            response.raise_for_status()
            return response.json()

    async def _execute_with_retry(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Execute request with exponential backoff retry logic."""
        delay = self.retry_delay

        for attempt in range(self.max_retries):
            try:
                return await self._execute_request(method, url, params, headers)

            except httpx.HTTPError as e:
                status_code = getattr(e.response, "status_code", None) if hasattr(e, "response") else None

                # Retry for retriable status codes
                if (
                    status_code in self.RETRIABLE_STATUS_CODES
                    and attempt < self.max_retries - 1
                ):
                    # Exponential backoff with jitter
                    jitter = delay * (0.9 + 0.2 * random.random())
                    logger.warning(
                        f"Retry attempt {attempt + 1} after {jitter:.2f}s (Status: {status_code})"
                    )
                    await asyncio.sleep(jitter)
                    delay *= 2  # Backoff multiplier
                    continue

                # Non-retriable error or max retries exceeded
                logger.error(f"Request failed: {e}")
                raise

        raise RuntimeError(f"Max retries ({self.max_retries}) exceeded")

    async def fetch_multiple(
        self,
        endpoints: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Fetch from multiple endpoints concurrently."""
        tasks = {
            name: self.get(endpoint, params)
            for name, (endpoint, params) in endpoints.items()
        }

        results = {}
        for name, task in tasks.items():
            try:
                results[name] = await task
            except httpx.HTTPError as e:
                logger.error(f"Error fetching {name}: {e}")
                results[name] = {"error": str(e)}

        return results

    async def fetch_paginated(
        self,
        endpoint: str,
        limit: int = 200,
        max_pages: Optional[int] = None,
        **params: Any,
    ) -> list:
        """Fetch all pages from a paginated endpoint."""
        all_results = []
        start = 0
        page = 0

        while True:
            if max_pages and page >= max_pages:
                break

            try:
                page_params = {**params, "start": start, "limit": limit}
                response = await self.get(endpoint, page_params)

                data = response.get("data", [])
                if not data:
                    break

                all_results.extend(data)
                start += limit
                page += 1

                logger.debug(f"Fetched page {page} ({len(data)} items)")

            except httpx.HTTPError as e:
                logger.error(f"Error fetching page {page}: {e}")
                break

        return all_results
