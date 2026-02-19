"""httpx-based HTTP client for the Tronscan API with retry logic."""

import logging
import random
import time
from typing import Any, Dict, Optional

import httpx

from src.config import Config

logger = logging.getLogger("tronscan")


class TronscanClient:
    """Thread-safe httpx client with retries, backoff, and courtesy delays."""

    def __init__(self, api_key: Optional[str] = None, verbose: bool = False) -> None:
        self._api_key = api_key or Config.API_KEY
        self._verbose = verbose
        self._client = httpx.Client(
            base_url=Config.BASE_URL,
            headers={
                "TRON-PRO-API-KEY": self._api_key,
                "Accept": "application/json",
            },
            timeout=Config.TIMEOUT,
        )

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a GET request with retry logic."""
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a POST request with retry logic."""
        return self._request("POST", path, json=json)

    def close(self) -> None:
        """Close the underlying httpx session."""
        self._client.close()

    def __enter__(self) -> "TronscanClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Execute request with exponential-backoff retry on transient errors."""
        # Remove None-valued params so they're not sent as "None" strings
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        attempt = 0
        delay = 1.0
        retriable = {408, 429, 500, 502, 503, 504}

        while True:
            t0 = time.monotonic()
            try:
                response = self._client.request(method, path, params=params, json=json)
                elapsed = time.monotonic() - t0

                if self._verbose:
                    logger.debug(
                        "%s %s → %s (%.2fs)",
                        method,
                        response.url,
                        response.status_code,
                        elapsed,
                    )
                else:
                    logger.info(
                        "%s %s (%s, %.2fs)",
                        method,
                        path,
                        response.status_code,
                        elapsed,
                    )

                if response.status_code in retriable and attempt < Config.MAX_RETRIES:
                    jitter = delay * 0.1 * (2 * random.random() - 1)
                    wait = delay + jitter
                    logger.warning(
                        "HTTP %s — retry %d/%d in %.1fs",
                        response.status_code,
                        attempt + 1,
                        Config.MAX_RETRIES,
                        wait,
                    )
                    time.sleep(wait)
                    delay *= Config.BACKOFF_MULTIPLIER
                    attempt += 1
                    continue

                response.raise_for_status()
                time.sleep(Config.COURTESY_DELAY)
                return response.json()

            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if status in {400, 401, 403, 404}:
                    raise SystemExit(
                        f"Error {status}: {exc.response.text}"
                    ) from exc
                raise

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                if attempt >= Config.MAX_RETRIES:
                    raise SystemExit(f"Network error after {Config.MAX_RETRIES} retries: {exc}") from exc
                jitter = delay * 0.1 * (2 * random.random() - 1)
                wait = delay + jitter
                logger.warning("Network error — retry %d/%d in %.1fs: %s", attempt + 1, Config.MAX_RETRIES, wait, exc)
                time.sleep(wait)
                delay *= Config.BACKOFF_MULTIPLIER
                attempt += 1
