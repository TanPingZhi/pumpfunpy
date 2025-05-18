import json
import pytest
from pumpfunpy import PumpFunAPI

# fartcoin: https://pump.fun/coin/9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump
MINT = "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"
LIMIT = 200


@pytest.fixture
def api():
    return PumpFunAPI()


def test_hello_world(api):
    assert api._frontend.hello_world() == "Hello World!"


def test_get_health(api):
    assert api._frontend.get_health() == {'status': 'ok'}


def test_get_sol_price(api):
    price = api.get_sol_price().get('solPrice', None)
    assert isinstance(price, float)


def test_list_trades(api):
    trades = api.list_trades(mint=MINT, limit=LIMIT, offset=0)
    assert isinstance(trades, list)
    assert len(trades) == LIMIT
    sample = trades[0]
    expected_keys = {
        "signature",
        "mint",
        "sol_amount",
        "token_amount",
        "is_buy",
        "user",
        "timestamp",
        "tx_index",
        "slot",
    }
    assert expected_keys.issubset(sample.keys())


def test_list_replies(api):
    response = api.list_replies(mint=MINT, limit=LIMIT, offset=0)
    assert isinstance(response, dict)
    assert "replies" in response
    assert isinstance(response["replies"], list)
    # Allow empty replies, but if non-empty, check the shape
    if response["replies"]:
        r = response["replies"][0]
        expected_keys = {
            "signature",
            "is_buy",
            "sol_amount",
            "id",
            "mint",
            "file_uri",
            "text",
            "user",
            "timestamp",
            "total_likes",
            "username",
            "profile_image",
            "liked_by_user"
        }
        assert expected_keys.issubset(r.keys())

    assert 'hasMore' in response
    assert 'offset' in response
