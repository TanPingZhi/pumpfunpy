from ..transport import HTTPClient


class AdvancedAPI:
    def __init__(self, client: HTTPClient):
        self._client = client

    def hello_world(self) -> dict:
        return self._client.request("GET", "/")

    def get_health(self) -> dict:
        return self._client.request("GET", "/health")

    def list_new_coins(self, last_score: int = 0) -> dict:
        return self._client.request("GET", "/coins/list", params={'lastScore': last_score, 'sortBy': 'creationTime'})

    def list_about_to_graduate_coins(self, last_score: int = 0) -> dict:
        return self._client.request("GET", "/coins/list", params={'lastScore': last_score, 'sortBy': 'marketCap'})

    def list_graduated_coins(self, last_score: int = 0) -> dict:
        return self._client.request("GET", "/coins/graduated", params={'lastScore': last_score})

    def list_featured_coins(self) -> dict:
        return self._client.request("GET", "/coins/featured")
