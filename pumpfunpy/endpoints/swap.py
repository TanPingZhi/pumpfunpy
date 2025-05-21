from ..transport import HTTPClient


class SwapAPI:

    def __init__(self, client: HTTPClient):
        self._client = client

    def get_candlesticks(
            self,
            mint: str,
            interval: str = "1m",  # “5s”, “1m”, “5m”
            limit: int = 1000,
            currency: str = "USD",
    ) -> list[dict]:
        return self._client.request(
            "GET",
            f"/v1/coins/{mint}/candles",
            params={
                "interval": interval,
                "limit": limit,
                "currency": currency,
            },
        )
