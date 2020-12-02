import pytest
import pandas as pd

from crypto_bot.puller.bitbay_api import BitbayApi


TICKER = 'btcpln'
COLUMNS = ['date', 'price', 'type', 'amount', 'tid']
JSON_DATA = [
    {"date": 1396094988, "price": 4500, "type": "buy", "amount": 0.0129, "tid": "0"},
    {"date": 1396096603, "price": 4400, "type": "sell", "amount": 0.011364, "tid": "1"},
]
EXPECTED = pd.DataFrame(
    data=[[row[key] for key in COLUMNS] for row in JSON_DATA],
    columns=COLUMNS
)


class MockResponse:
    def json(self):
        return JSON_DATA


class EmptyMockResponse:
    def json(self):
        return {}


def test_bitbay_api(mocker):
    mocker.patch('requests.Session.get', side_effect=[MockResponse(), EmptyMockResponse()])
    trades = BitbayApi().get_all_trades(ticker=TICKER)
    assert next(trades).equals(EXPECTED)
    with pytest.raises(StopIteration):
        next(trades)
