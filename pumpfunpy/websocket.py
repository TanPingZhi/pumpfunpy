import asyncio
import json
import websockets
from .exceptions import WebSocketError


class WebSocketClient:
    def __init__(self, url: str, heartbeat: float = 30.0):
        self.url = url
        self.heartbeat = heartbeat
        self._ws = None
        self._keepalive_task = None

    async def connect(self):
        try:
            self._ws = await websockets.connect(self.url)
        except Exception as exc:
            raise WebSocketError(f"Failed to connect: {exc}")
        self._keepalive_task = asyncio.create_task(self._keepalive())

    async def _keepalive(self):
        try:
            while True:
                await asyncio.sleep(self.heartbeat)
                await self._ws.ping()
        except Exception as exc:
            # ignore; user should handle reconnection
            return

    async def subscribe(self, channel: str):
        if not self._ws:
            raise WebSocketError("WebSocket is not connected")
        await self._ws.send(json.dumps({"op": "subscribe", "channel": channel}))

    async def listen(self):
        if not self._ws:
            raise WebSocketError("WebSocket is not connected")
        async for message in self._ws:
            yield json.loads(message)

    async def close(self):
        if self._keepalive_task:
            self._keepalive_task.cancel()
        if self._ws:
            await self._ws.close()
