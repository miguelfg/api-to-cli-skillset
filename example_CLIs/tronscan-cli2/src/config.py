"""Configuration management for tronscan-cli."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")


class Config:
    """Centralised configuration loaded from environment / .env."""

    BASE_URL: str = os.getenv("TRONSCAN_BASE_URL", "https://apilist.tronscanapi.com")
    API_KEY: str = os.getenv("TRONSCAN_API_KEY", "")
    TIMEOUT: int = int(os.getenv("TRONSCAN_TIMEOUT", "30"))
    LOG_LEVEL: str = os.getenv("TRONSCAN_LOG_LEVEL", "INFO").upper()
    CACHE_DIR: str = os.getenv("TRONSCAN_CACHE_DIR", "./cache")
    OUTPUT_DIR: str = os.getenv("TRONSCAN_OUTPUT_DIR", "./output")
    TIMESTAMP_FORMAT: str = os.getenv("TRONSCAN_TIMESTAMP_FORMAT", "%Y%m%d_%H%M%S")

    # Retry settings
    MAX_RETRIES: int = int(os.getenv("TRONSCAN_MAX_RETRIES", "3"))
    BACKOFF_MULTIPLIER: float = float(os.getenv("TRONSCAN_BACKOFF_MULTIPLIER", "2.0"))
    COURTESY_DELAY: float = float(os.getenv("TRONSCAN_COURTESY_DELAY", "0.1"))

    @classmethod
    def validate(cls) -> None:
        """Raise ValueError if required config is missing."""
        if not cls.API_KEY:
            raise ValueError(
                "TRONSCAN_API_KEY is not set.\n"
                "Set it via:\n"
                "  export TRONSCAN_API_KEY=your-tron-pro-api-key\n"
                "  or add it to your .env file"
            )
