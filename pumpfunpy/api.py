import asyncio # need aiohttp to run this
import json
from typing import AsyncIterator

import socketio
import websockets

from .transport import HTTPClient
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

            while True:
                msg = await ws.recv(decode=True)
                # msg = msg.decode("utf-8")
                # Server‐side heartbeat
                if msg.strip() == "PING":
                    await ws.send("PONG\r\n")
                    continue

                if msg.startswith("MSG newCoinCreated.prod"):
                    # The new coin is in the second line of the message
                    payload = msg.split("\r\n", 2)[1]
                    yield json.loads(payload)
