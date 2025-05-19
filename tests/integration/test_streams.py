import asyncio
import pytest

from pumpfunpy.api import PumpFunAPI

async def _drain(agen, collector: list, limit: int):
    """
    Helper: pull up to `limit` items from async generator `agen`
    into `collector`, then return.
    """
    async for item in agen:
        collector.append(item)
        if len(collector) >= limit:
            return

@pytest.mark.asyncio
async def test_stream_new_coins():
    api = PumpFunAPI()
    agen = api.stream_new_coins()
    seen = []

    try:
        # try to collect 3 coins within 20 seconds
        await asyncio.wait_for(_drain(agen, seen, 3), timeout=20)
    except asyncio.TimeoutError:
        pytest.skip("Timed out waiting for new-coin events; maybe the market is slow")

    # cleanup
    await agen.aclose()

    # Assertions
    assert len(seen) == 3
    for coin in seen:
        assert isinstance(coin, dict)
        for key in ("mint", "name", "symbol", "created_timestamp"):
            assert key in coin

@pytest.mark.asyncio
async def test_stream_all_trades():
    api = PumpFunAPI()
    agen = api.stream_all_trades()
    seen = []

    try:
        # try to collect 3 trades within 20 seconds
        await asyncio.wait_for(_drain(agen, seen, 3), timeout=20)
    except asyncio.TimeoutError:
        pytest.skip("Timed out waiting for trade events; check network or market activity")

    # cleanup
    await agen.aclose()

    assert len(seen) == 3
    for trade in seen:
        assert isinstance(trade, dict)
        for key in ("signature", "mint", "sol_amount", "token_amount", "is_buy", "timestamp"):
            assert key in trade
