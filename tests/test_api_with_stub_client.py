# import pytest
# from pumpfunpy import HTTPClient
# from pumpfunpy.api import PumpFunAPI
#
#
# class StubHTTPClient(HTTPClient):
#     def __init__(self):
#         super().__init__()
#         self.calls = []
#
#     def request(self, method, endpoint, **kwargs):
#         self.calls.append((method, endpoint, kwargs))
#         return {"endpoint": endpoint, "kwargs": kwargs}
#
#
# @pytest.fixture
# def stub_api():
#     stub = StubHTTPClient()
#     return PumpFunAPI(client=stub)
#
#
# def test_hello_world(stub_api):
#     out = stub_api.hello_world()
#     assert out == {"endpoint": "/", "kwargs": {}}
#
#
# def test_get_health(stub_api):
#     assert stub_api.get_health() == {"endpoint": "/health", "kwargs": {}}
#
#
# def test_get_latest_trades(stub_api):
#     assert stub_api.get_latest_trades() == {"endpoint": "/trades/latest", "kwargs": {}}
#
#
# def test_get_all_trades_params(stub_api):
#     result = stub_api.get_all_trades("MINT1", limit=10, offset=2, minimum_size=5)
#     # check return value
#     assert result["endpoint"] == "/trades/all/MINT1"
#     # inspect what was passed to the client
#     method, endpoint, kwargs = stub_api._client.calls[-1]
#     assert method == "GET"
#     assert endpoint == "/trades/all/MINT1"
#     assert kwargs["params"] == {
#         "limit": 10,
#         "offset": 2,
#         "minimumSize": 5
#     }
