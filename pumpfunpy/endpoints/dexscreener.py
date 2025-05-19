from ..transport import HTTPClient
from ..config import DEXSCREENER_BASE_URL
from ..exceptions import APIRequestError

class DexScreenerAPI:
    def __init__(self, client: HTTPClient = None):
        # base_url ends up "https://api.dexscreener.com"
        self._client = client or HTTPClient(DEXSCREENER_BASE_URL)

    def get_pool_for_mint(self, mint: str) -> str:
        """
        Calls GET /tokens/v1/solana/{mint} and returns the first
        'pairAddress' in the array.
        """
        resp = self._client.request("GET", f"/tokens/v1/solana/{mint}")
        if not isinstance(resp, list) or not resp:
            raise APIRequestError(f"No pool found for mint {mint}")
        return resp[0]["pairAddress"]