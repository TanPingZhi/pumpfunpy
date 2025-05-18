import pytest
from pumpfunpy import PumpFunAPI


@pytest.fixture
def api():
    return PumpFunAPI()


def test_hello_world(api):
    assert api._frontend.hello_world() == "Hello World!"


def test_get_health(api):
    assert api._frontend.get_health() == {'status': 'ok'}


def test_list_new_coins(api):
    out = api.list_new_coins()
    assert 'coins' in out
    assert 'pagination' in out
    assert 'lastScore' in out['pagination']
    assert 'hasMore' in out['pagination']


def test_list_about_to_graduate_coins(api):
    out = api.list_about_to_graduate_coins()
    assert 'coins' in out
    assert 'pagination' in out
    assert 'lastScore' in out['pagination']
    assert 'hasMore' in out['pagination']


def test_list_graduated_coins(api):
    out = api.list_graduated_coins()
    assert 'coins' in out
    assert 'pagination' in out
    assert 'lastScore' in out['pagination']
    assert 'hasMore' in out['pagination']


def test_list_featured_coins(api):
    out = api.list_featured_coins()
    assert 'coins' in out
    assert 'pagination' in out
    assert 'offset' in out['pagination']
    assert 'limit' in out['pagination']
    assert 'hasMore' in out['pagination']
