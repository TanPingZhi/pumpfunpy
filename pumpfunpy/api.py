import asyncio  # need aiohttp to run this
import contextlib
import json
from typing import AsyncIterator

import socketio
import websockets

from .endpoints.swap import SwapAPI
from .transport import HTTPClient
from .config import API_VERSIONS
from .endpoints.advanced import AdvancedAPI
from .endpoints.frontend import FrontendAPI
from .utils import json_deep_loads


class PumpFunAPI:

    def __init__(self,
                 _frontend_client: HTTPClient = None,
                 _advanced_client: HTTPClient = None,
                 _swap_client: HTTPClient = None,
                 ):
        self._frontend = FrontendAPI(_frontend_client or HTTPClient(API_VERSIONS['frontend_v3']))
        self._advanced = AdvancedAPI(_advanced_client or HTTPClient(API_VERSIONS['advanced_v2']))
        self._swap = SwapAPI(_swap_client or HTTPClient(API_VERSIONS["swap_v1"]))

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

    def get_candlesticks(
            self,
            mint: str,
            interval: str = "1m",
            limit: int = 1000,
            currency: str = "USD",
    ) -> list[dict]:
        return self._swap.get_candlesticks(
            mint=mint,
            interval=interval,
            limit=limit,
            currency=currency,
        )

    async def stream_all_trades(self) -> AsyncIterator[dict]:
        queue: asyncio.Queue = asyncio.Queue()
        sio = socketio.AsyncClient(logger=False, engineio_logger=False)

        @sio.on("tradeCreated")
        async def _(data):
            await queue.put(data)

        await sio.connect(
            API_VERSIONS['frontend_v3'],
            transports=["websocket"],
        )

        try:
            while True:
                trade = await queue.get()
                yield trade
        finally:
            await sio.disconnect()

    async def stream_new_coins(self) -> AsyncIterator[dict]:
        uri = "wss://prod-v2.nats.realtime.pump.fun/"
        async with websockets.connect(uri) as ws:

            # Send the NATS CONNECT handshake
            connect_payload = {
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
            await ws.send("CONNECT " + json.dumps(connect_payload) + "\r\n")
            await ws.send("PING\r\n")
            await ws.recv()  # Should be "PONG\r\n"

            # Subscribe to the new‐coin subject
            await ws.send("SUB newCoinCreated.prod 1\r\n")

            async def _keepalive(interval: float = 30.0):
                try:
                    while True:
                        await asyncio.sleep(interval)
                        await ws.send("PING\r\n")
                except asyncio.CancelledError:
                    # normal shutdown
                    pass

            ka_task = asyncio.create_task(_keepalive())

            try:
                while True:

                    msg = await ws.recv(decode=True)
                    # Server‐side heartbeat
                    if msg.strip() == "PING":
                        await ws.send("PONG\r\n")
                        continue

                    if msg.startswith("MSG newCoinCreated.prod"):
                        # The new coin is in the second line of the message
                        payload = msg.split("\r\n", 2)[1]
                        yield json_deep_loads(payload)
            finally:
                ka_task.cancel()
                # optionally await ka_task to silence warnings
                with contextlib.suppress(asyncio.CancelledError):
                    await ka_task

    async def stream_new_replies(self, mint: str) -> AsyncIterator[dict]:
        uri = "wss://prod-v2.nats.realtime.pump.fun/"
        async with websockets.connect(uri) as ws:

            # 1) NATS CONNECT handshake
            connect_payload = {
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
            await ws.send("CONNECT " + json.dumps(connect_payload) + "\r\n")
            # prime the first heartbeat
            await ws.send("PING\r\n")
            await ws.recv()  # expect "PONG\r\n"

            # 2) subscribe to replies
            await ws.send(f"SUB newReplyCreated.{mint}.prod 1\r\n")

            # 3) spawn keep-alive task
            async def _keepalive(interval: float = 30.0):
                try:
                    while True:
                        await asyncio.sleep(interval)
                        await ws.send("PING\r\n")
                except asyncio.CancelledError:
                    # normal shutdown
                    pass

            ka_task = asyncio.create_task(_keepalive())

            try:
                # 4) main read loop
                while True:
                    msg = await ws.recv(decode=True)

                    # server-side heartbeat
                    if msg.strip() == "PING":
                        await ws.send("PONG\r\n")
                        continue

                    # your actual payloads
                    if msg.startswith("MSG newReplyCreated"):
                        payload = msg.split("\r\n", 2)[1]
                        yield json_deep_loads(payload)['replyPayload']

            finally:
                ka_task.cancel()
                # optionally await ka_task to silence warnings
                with contextlib.suppress(asyncio.CancelledError):
                    await ka_task

# streaming the price / trades of a single coin is not possible need to use the all_trades endpoint
