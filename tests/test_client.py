# import pytest
# import requests
# from pumpfunpy.transport import HTTPClient
# from pumpfunpy.exceptions import APIRequestError
#
# # A dummy Response‐like object
# class DummyResponse:
#     def __init__(self, status_code=200, json_data=None, text_data=""):
#         self.status_code = status_code
#         self._json = json_data
#         self.text = text_data
#
#     def raise_for_status(self):
#         if self.status_code >= 400:
#             raise requests.HTTPError(f"HTTP {self.status_code}")
#
#     def json(self):
#         if self._json is None:
#             raise ValueError("No JSON")
#         return self._json
#
# def test_request_success_json(monkeypatch):
#     dummy = DummyResponse(status_code=200, json_data={"foo": "bar"})
#     monkeypatch.setattr("requests.request", lambda *args, **kwargs: dummy)
#
#     client = HTTPClient(base_url="https://example.com", timeout=5)
#     res = client.request("GET", "/test", params={"a": 1})
#     assert res == {"foo": "bar"}
#
# def test_request_success_text(monkeypatch):
#     dummy = DummyResponse(status_code=200, json_data=None, text_data="plain text")
#     monkeypatch.setattr("requests.request", lambda *args, **kwargs: dummy)
#
#     client = HTTPClient()
#     res = client.request("GET", "/")
#     assert res == "plain text"
#
# def test_request_http_exception(monkeypatch):
#     def fake_request(*args, **kwargs):
#         raise requests.RequestException("timeout")
#     monkeypatch.setattr("requests.request", fake_request)
#
#     client = HTTPClient()
#     with pytest.raises(APIRequestError):
#         client.request("GET", "/")
#
# def test_request_status_error(monkeypatch):
#     dummy = DummyResponse(status_code=500, json_data={"error": "fail"})
#     monkeypatch.setattr("requests.request", lambda *args, **kwargs: dummy)
#
#     client = HTTPClient()
#     with pytest.raises(APIRequestError):
#         client.request("GET", "/")
