from pytest_mock import MockerFixture

from crypto_bot.puller.controller import Puller
from crypto_bot.puller.queries import Queries


JSON_DATA = [
    {"date": 1, "price": 33, "type": "sell", "amount": 0.011364, "tid": "1"},
    {"date": 2, "price": 44, "type": "buy", "amount": 0.5, "tid": "2"},
]
TICKER_ID = 0
DATA_TO_INSERT = [['1', 1, 33, 0.011364, TICKER_ID], ['2', 2, 44, 0.5, TICKER_ID]]
TICKERS = ['btcpln']


class MockResp():
    def json(self):
        return JSON_DATA


class EmptyMockResp():
    def json(self):
        return {}


def test_puller(mocker: MockerFixture) -> None:
    mocker.patch('crypto_bot.puller.queries.Queries.select_id_by_ticker', return_value=[TICKER_ID])
    mocker.patch('crypto_bot.puller.queries.Queries.select_last_transaction_tid', return_value=[0])
    mocker.patch('requests.Session.get', side_effect=[MockResp(), EmptyMockResp()])

    queries = Queries(mocker.Mock())
    spy = mocker.spy(queries, 'insert_trade')

    Puller()._pull_trades(queries, tickers=TICKERS)
    spy.assert_called_once_with(bulk_values=DATA_TO_INSERT)
