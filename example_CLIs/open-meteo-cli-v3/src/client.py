"""
API Client Library - Auto-generated from PRD.md
"""

import requests
from typing import Dict, Any, Optional
from src.config import Config


class APIClient:
    """HTTP client for open-meteo Python Client - Product Requirements Document."""

    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.get('base_url', 'https://api.example.com')
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        """Configure authentication headers."""
        auth_methods = []

        if 'api_key' in auth_methods:
            api_key = self.config.get('api_key', '')
            if api_key:
                self.session.headers.update({'X-API-Key': api_key})

        if 'bearer_token' in auth_methods:
            token = self.config.get('api_token', '')
            if token:
                self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute GET request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """Execute POST request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """Execute PUT request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Execute DELETE request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, timeout=30)
        response.raise_for_status()
        return response.json() if response.text else {"status": "deleted"}
