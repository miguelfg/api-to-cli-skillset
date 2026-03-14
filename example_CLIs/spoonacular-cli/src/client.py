"""
API Client Library - Auto-generated from PRD.md
"""

from typing import Dict, Any, Optional
import requests
from src.config import Config


class APIClient:
    """HTTP client for Spoonacular Food API Python Client - Product Requirements Document using requests."""

    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.get('base_url', 'https://api.spoonacular.com')
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        api_key = self.config.get('api_key', '')
        if api_key:
            # Spoonacular documents both x-api-key and apiKey query-param auth.
            self.session.headers.update({'x-api-key': api_key})

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        params = dict(params or {})
        if self.config.get('api_key') and 'apiKey' not in params:
            params['apiKey'] = self.config.get('api_key')
        response = self.session.request(method=method, url=url, params=params, json=data, timeout=30)
        response.raise_for_status()
        if not response.text:
            return {}
        return response.json()

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        return self._request('POST', endpoint, data=data)

    def put(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        return self._request('PUT', endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        result = self._request('DELETE', endpoint)
        return result if result else {"status": "deleted"}
