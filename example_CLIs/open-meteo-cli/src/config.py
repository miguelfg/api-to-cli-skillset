"""
Configuration management for the CLI.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Load and manage configuration from .env and config files."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path('.env')
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from .env file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value

    def save(self):
        """Save configuration to .env file."""
        with open(self.config_path, 'w') as f:
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")
