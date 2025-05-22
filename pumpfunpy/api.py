import asyncio  # need aiohttp to run this
import contextlib
import json
from typing import AsyncIterator

import socketio
import websockets

from .endpoints.dexscreener import DexScreenerAPI
from .endpoints.swap import SwapAPI
from .transport import HTTPClient
from .config import API_VERSIONS
from .endpoints.advanced import AdvancedAPI
from .endpoints.frontend import FrontendAPI
from .utils import json_deep_loads
from .streamers import make_streamer


class PumpFunAPI:

    def __init__(self,
                 _frontend_client: HTTPClient = None,
                 _advanced_client: HTTPClient = None,
                 _swap_client: HTTPClient = None,
                 streamer_factory=make_streamer
                 ):
        self._frontend = FrontendAPI(_frontend_client or HTTPClient(API_VERSIONS['frontend_v3']))
        self._advanced = AdvancedAPI(_advanced_client or HTTPClient(API_VERSIONS['advanced_v2']))
        self._swap = SwapAPI(_swap_client or HTTPClient(API_VERSIONS["swap_v1"]))
        self._make_streamer = streamer_factory

    def list_trades(self, mint: str, limit: int, offset: int = 0, minimum_size: int = 0) -> list:
        return self._frontend.list_trades(mint, limit, offset, minimum_size)

    def list_replies(self, mint: str, limit: int, offset: int = 0) -> dict:
        return self._frontend.list_replies(mint, limit, offset)

    def get_sol_price(self):  # note: this is delayed price
        return self._frontend.get_sol_price()

    def get_coin_info(self, mint: str) -> dict:
        return self._frontend.get_coin_info(mint)

    def get_price_in_sol(self, mint: str) -> float:
        return float(self.get_candlesticks(mint, limit=1, currency='SOL')[-1]['close'])

    def get_market_cap(self, mint: str) -> float:
        return self._frontend.get_market_cap(mint)

    def has_graduated(self, mint: str) -> bool:
        return self._frontend.has_graduated(mint)

    def list_new_coins(self, last_score: int = 0) -> dict:
        return self._advanced.list_new_coins(last_score)

    def list_about_to_graduate_coins(self, last_score: int = 0) -> dict:
        return self._advanced.list_about_to_graduate_coins(last_score)

    # returns {'coins': [...], 'pagination': {'lastScore': ..., 'hasMore': True / False}}
    def list_graduated_coins(self, last_score: int = 0) -> dict:
        return self._advanced.list_graduated_coins(last_score)

    def list_featured_coins(self) -> dict:
        return self._advanced.list_featured_coins()

    # this function is only for non grad coins
    def get_candlesticks(self, mint: str, interval: str = "1m", limit: int = 1000, currency: str = "USD", ) -> list[
        dict]:
        return self._swap.get_candlesticks(mint=mint, interval=interval, limit=limit, currency=currency, )

    async def stream_all_trades(self) -> AsyncIterator[dict]:
        streamer = self._make_streamer(
            kind="io",
            url=API_VERSIONS['frontend_v3'],
            event="tradeCreated"
        )
        async with streamer as s:
            async for msg in s:
                yield msg

    async def stream_new_coins(self) -> AsyncIterator[dict]:
        payload = {
            "no_responders": True,
            "protocol": 1,
            "verbose": False,
            "pedantic": False,
            "user": "subscriber",
            "pass": "lW5a9y20NceF6AE9",
            "lang": "nats.ws",
            "version": "1.29.2",
            "headers": True,
        }
        streamer = self._make_streamer(
            kind="nats",
            uri="wss://prod-v2.nats.realtime.pump.fun/",
            connect_payload=payload,
            subject="newCoinCreated.prod"
        )
        async with streamer as s:
            async for msg in s:
                yield json_deep_loads(msg)

    async def stream_new_replies(self, mint: str) -> AsyncIterator[dict]:
        payload = {
            "no_responders": True,
            "protocol": 1,
            "verbose": False,
            "pedantic": False,
            "user": "subscriber",
            "pass": "lW5a9y20NceF6AE9",
            "lang": "nats.ws",
            "version": "1.29.2",
            "headers": True,
        }
        streamer = self._make_streamer(
            kind="nats",
            uri="wss://prod-v2.nats.realtime.pump.fun/",
            connect_payload=payload,
            subject=f"newReplyCreated.{mint}.prod"
        )
        async with streamer as s:
            async for msg in s:
                yield json_deep_loads(msg)["replyPayload"]

    async def stream_graduated_coin_trades(self, mint: str) -> AsyncIterator[dict]:
        pool_id = DexScreenerAPI().get_pool_for_mint(mint)
        payload = {
            "no_responders": True,
            "protocol": 1,
            "verbose": False,
            "pedantic": False,
            "user": "subscriber",
            "pass": "7wjQpG3JvSQbUg3X",
            "lang": "nats.ws",
            "version": "1.29.2",
            "headers": True,
        }
        streamer = self._make_streamer(
            kind="nats",
            uri="wss://amm-prod.nats.realtime.pump.fun/",
            connect_payload=payload,
            subject=f"ammTradeEvent.{pool_id}"
        )
        async with streamer as s:
            async for msg in s:
                yield json_deep_loads(msg)

# streaming the price / trades of a single coin is not possible need to use the all_trades endpoint
