from .endpoints import frontend
from .transport import HTTPClient
from .websocket import WebSocketClient
from .config import API_VERSIONS
from .endpoints.advanced import AdvancedAPI
from .endpoints.frontend import FrontendAPI


class PumpFunAPI:

    def __init__(self,
                 _frontend_client: HTTPClient = None,
                 _advanced_client: HTTPClient = None,
                 ):
        self._frontend = FrontendAPI(_frontend_client or HTTPClient(API_VERSIONS['frontend_v3']))
        self._advanced = AdvancedAPI(_advanced_client or HTTPClient(API_VERSIONS['advanced_v2']))

    def list_trades(self, mint: str, limit: int, offset: int = 0, minimum_size: int = 0) -> list:
        return self._frontend.list_trades(mint, limit, offset, minimum_size)

    def list_replies(self, mint: str, limit: int, offset: int = 0) -> dict:
        return self._frontend.list_replies(mint, limit, offset)

    def get_sol_price(self):  # note: this is delayed price
        return self._frontend.get_sol_price()

    def list_new_coins(self, last_score: int = 0) -> dict:
        return self._advanced.list_new_coins(last_score)

    def list_about_to_graduate_coins(self, last_score: int = 0) -> dict:
        return self._advanced.list_about_to_graduate_coins(last_score)

    # returns {'coins': [...], 'pagination': {'lastScore': ..., 'hasMore': True / False}}
    def list_graduated_coins(self, last_score: int = 0) -> dict:
        return self._advanced.list_graduated_coins(last_score)

    def list_featured_coins(self) -> dict:
        return self._advanced.list_featured_coins()

    # Need to test this
    # def live_trades_client(self, url: str = None) -> WebSocketClient:
    #     ws_url = (url or self._client.base_url.replace("https://", "wss://")) + "/ws/trades"
    #     return WebSocketClient(ws_url)

    def post_reply(self):
        pass
