import json
import pytest
from pumpfunpy import PumpFunAPI


MINT = "FqBFkE33JuPXga9EtREkidHEXj9UwFmgEZCLQkucCh28"

@pytest.fixture
def api():
    return PumpFunAPI()

def test_get_candlesticks(api):
    response = api.get_candlesticks(MINT, limit=1)
    print(json.dumps(response, indent=4))

    assert True