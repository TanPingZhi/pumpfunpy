import json
import pytest
from pumpfunpy import PumpFunAPI

# fartcoin: https://pump.fun/coin/9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump
MINT = "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"

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

# upto 200 trades
def test_list_trades(api):
    MINT = 'AtSyNFCLenHGgoDKJQiLCfKmGf4QUq4BAYcgJzeCpump'
    trades = api.list_trades(mint=MINT, limit=200, offset=0)
    assert isinstance(trades, list)
    assert len(trades) == 200
    sample = trades[0]
    print(json.dumps(sample, indent=4))
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

# upto 1000 replies
def test_list_replies(api):
    response = api.list_replies(mint=MINT, limit=1000, offset=0)
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

def test_get_price_in_sol(api):
    # price = api.get_price_in_sol(MINT)
    m = "6HZyKuvApDJ4pMqSL7TVwjNixoQWqBQcvDX4ayNBpump"
    price = api.get_price_in_sol(m)
    info = api.get_coin_info(m)
    print(json.dumps(info, indent=4))
    print(json.dumps(price, indent=4))
    assert isinstance(price, float)
    assert price > 0