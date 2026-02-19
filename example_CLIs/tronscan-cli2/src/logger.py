"""Logging setup for tronscan-cli (screen only)."""

import logging
import sys

from src.config import Config


def setup_logger(name: str = "tronscan", verbose: bool = False) -> logging.Logger:
    """Configure and return the application logger.

    Args:
        name: Logger name.
        verbose: If True, set level to DEBUG regardless of config.

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured — avoid duplicate handlers
        return logger

    level = logging.DEBUG if verbose else getattr(logging, Config.LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Screen handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
