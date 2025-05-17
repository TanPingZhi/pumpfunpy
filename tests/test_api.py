# import pytest
# from pumpfunpy import PumpFunAPI
# import json
#
# @pytest.fixture
# def api():
#     return PumpFunAPI()
#
#
# def test_hello_world(api):
#     assert api.hello_world() == "Hello World!"
#
#
# def test_get_health(api):
#     assert api.get_health() == {'status': 'ok'}
#
#
# def test_list_trades(api):
#     # fartcoin: https://pump.fun/coin/9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump
#     out = api.list_trades(mint='9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump', limit=200, offset=0)
#     print(out)
#     assert len(out) == 200
#
# def test_list_replies(api):
#     # fartcoin: https://pump.fun/coin/9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump
#     out = api.list_replies("9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump", 5)
#
#     assert True