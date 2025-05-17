import requests
from .config import DEFAULT_HEADERS, DEFAULT_TIMEOUT
from .exceptions import APIRequestError


class HTTPClient:

    def __init__(self,
                 base_url: str,
                 headers: dict = DEFAULT_HEADERS,
                 timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def request(self,
                method: str,
                endpoint: str,
                params: dict = None,
                data: dict = None,
                json: dict = None):
        try:
            response = requests.request(
                method=method,
                url=self.base_url + endpoint,
                headers=self.headers,
                timeout=self.timeout,
                params=params,
                data=data,
                json=json,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise APIRequestError(f"Request to {endpoint} failed: {e}")
        try:
            return response.json()
        except ValueError:
            return response.text
