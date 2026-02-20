"""
API Client Library - Auto-generated from PRD.md
"""

from typing import Dict, Any, Optional
import requests
from src.config import Config


class APIClient:
    """HTTP client for PRD: Arkham Intel API Python CLI Client using requests."""

    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.get('base_url', 'https://intel.arkm.com/api')
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        auth_methods = []
        if 'api_key' in auth_methods:
            api_key = self.config.get('api_key', '')
            if api_key:
                self.session.headers.update({'X-API-Key': api_key})
        if 'bearer_token' in auth_methods:
            token = self.config.get('api_token', '')
            if token:
                self.session.headers.update({'Authorization': f'Bearer {token}'})

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
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
