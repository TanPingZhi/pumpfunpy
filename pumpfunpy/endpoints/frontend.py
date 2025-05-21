from ..transport import HTTPClient


class FrontendAPI:
    def __init__(self, client: HTTPClient):
        self._client = client

    def hello_world(self) -> dict:
        return self._client.request("GET", "/")

    def get_health(self) -> dict:
        return self._client.request("GET", "/health")

    def get_sol_price(self) -> dict:
        return self._client.request("GET", "/sol-price")

    def list_trades(self, mint: str, limit: int, offset: int = 0, minimum_size: int = 0) -> list:
        return self._client.request(
            "GET",
            f"/trades/all/{mint}",
            params={"limit": limit, "offset": offset, "minimumSize": minimum_size},
        )

    def list_replies(self, mint: str, limit: int, offset: int = 0, reverse_order: bool = True) -> dict:
        return self._client.request(
            "GET",
            f"/replies/{mint}",
            params={"limit": limit, "offset": offset, "reverseOrder": reverse_order},
        )

    def get_coin_info(self, mint: str) -> dict:
        return self._client.request("GET", f"/coins/{mint}")

    def get_market_cap(self, mint: str) -> float:
        coin = self.get_coin_info(mint)
        return coin["market_cap"]

    def has_graduated(self, mint: str) -> bool:
        coin = self.get_coin_info(mint)
        return coin["complete"]
