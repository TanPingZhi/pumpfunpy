# pumpfunpy/streamers.py
from abc import ABC, abstractmethod
import asyncio
import json
import websockets
import socketio
from typing import AsyncIterator, Any

class Streamer(ABC, AsyncIterator[dict]):
    """
    Abstract base for any async streamer yielding dict messages.
    """
    @abstractmethod
    async def __aenter__(self) -> "Streamer":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        pass

    @abstractmethod
    async def __anext__(self) -> dict:
        pass


class SocketIOStreamer(Streamer):
    def __init__(self, url: str, event: str):
        self._url = url
        self._event = event
        self._sio = socketio.AsyncClient(logger=False, engineio_logger=False)

    async def __aenter__(self) -> "SocketIOStreamer":
        self._queue: asyncio.Queue = asyncio.Queue()

        @self._sio.on(self._event)
        async def _handler(data):
            await self._queue.put(data)

        await self._sio.connect(self._url, transports=["websocket"])
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self._sio.disconnect()

    async def __anext__(self) -> dict:
        return await self._queue.get()


class NatsStreamer(Streamer):
    def __init__(self, uri: str, connect_payload: dict, subject: str):
        self._uri = uri
        self._connect_payload = connect_payload
        self._subject = subject
        self._ws = None
        self._keep_task = None

    async def __aenter__(self) -> "NatsStreamer":
        self._ws = await websockets.connect(self._uri)
        await self._ws.send("CONNECT " + json.dumps(self._connect_payload) + "\r\n")
        await self._ws.send("PING\r\n")
        await self._ws.recv()
        await self._ws.send(f"SUB {self._subject} 1\r\n")

        # start keep-alive
        self._keep_task = asyncio.create_task(self._keepalive())
        return self

    async def _keepalive(self, interval: float = 30.0) -> None:
        try:
            while True:
                await asyncio.sleep(interval)
                await self._ws.send("PING\r\n")
        except asyncio.CancelledError:
            pass

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._keep_task:
            self._keep_task.cancel()
        if self._ws:
            await self._ws.close()

    async def __anext__(self) -> dict:
        while True:
            raw = await self._ws.recv(decode=True)
            if raw.strip() == "PING":
                await self._ws.send("PONG\r\n")
                continue

            prefix = f"MSG {self._subject}"
            if raw.startswith(prefix):
                # payload is the second line
                payload = raw.split("\r\n", 2)[1]
                return json.loads(payload)

def make_streamer(kind: str, **cfg) -> Streamer:
    if kind == "io":
        return SocketIOStreamer(url=cfg.pop("url"), event=cfg.pop("event"))
    elif kind == "nats":
        return NatsStreamer(
            uri=cfg.pop("uri"),
            connect_payload=cfg.pop("connect_payload"),
            subject=cfg.pop("subject")
        )
    else:
        raise ValueError(f"Unknown streamer kind: {kind}")