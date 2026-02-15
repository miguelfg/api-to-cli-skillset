"""Configuration management for Tronscan CLI."""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class Config:
    """Load and manage configuration from .env and config file."""

    DEFAULT_BASE_URL = "https://apilist.tronscan.org"
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1.0
    DEFAULT_LOG_LEVEL = "INFO"

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration from .env file."""
        self.config_file = env_file or ".env"
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from .env file."""
        config = {
            "TRONSCAN_BASE_URL": self.DEFAULT_BASE_URL,
            "TRONSCAN_API_KEY": None,
            "TRONSCAN_TIMEOUT": self.DEFAULT_TIMEOUT,
            "TRONSCAN_RETRIES": self.DEFAULT_RETRIES,
            "TRONSCAN_RETRY_DELAY": self.DEFAULT_RETRY_DELAY,
            "TRONSCAN_LOG_LEVEL": self.DEFAULT_LOG_LEVEL,
        }

        # Load from .env file if exists
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            config[key.strip()] = value.strip()

        # Override with environment variables
        for key in config:
            env_value = os.getenv(key)
            if env_value:
                config[key] = env_value

        return config

    @property
    def base_url(self) -> str:
        """Get API base URL."""
        return self._config.get("TRONSCAN_BASE_URL", self.DEFAULT_BASE_URL)

    @property
    def api_key(self) -> Optional[str]:
        """Get API key."""
        return self._config.get("TRONSCAN_API_KEY")

    @property
    def timeout(self) -> int:
        """Get request timeout."""
        return int(self._config.get("TRONSCAN_TIMEOUT", self.DEFAULT_TIMEOUT))

    @property
    def retries(self) -> int:
        """Get max retries."""
        return int(self._config.get("TRONSCAN_RETRIES", self.DEFAULT_RETRIES))

    @property
    def retry_delay(self) -> float:
        """Get initial retry delay."""
        return float(self._config.get("TRONSCAN_RETRY_DELAY", self.DEFAULT_RETRY_DELAY))

    @property
    def log_level(self) -> str:
        """Get log level."""
        return self._config.get("TRONSCAN_LOG_LEVEL", self.DEFAULT_LOG_LEVEL)

    @property
    def headers(self) -> Dict[str, str]:
        """Get HTTP headers with API key."""
        headers = {"User-Agent": "Tronscan-Python-CLI/1.0"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.base_url:
            logger.error("TRONSCAN_BASE_URL not configured")
            return False
        return True


def setup_logging(level: str = "INFO"):
    """Configure logging."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("tronscan_cli.log"),
        ],
    )

    return logging.getLogger(__name__)
