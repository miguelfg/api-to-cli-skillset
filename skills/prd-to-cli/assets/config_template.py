"""
Configuration management for generated CLI projects.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from src.utils import parse_env_value


class Config:
    """Load and manage key/value configuration from a .env-style file."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path(".env")
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration values from file."""
        self.config = {}
        if not self.config_path.exists():
            return

        with open(self.config_path, encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                self.config[key.strip()] = parse_env_value(value.strip())

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value

    def save(self):
        """Persist configuration values to disk."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")
