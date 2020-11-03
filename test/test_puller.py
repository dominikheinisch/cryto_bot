from pytest_mock import mocker, MockerFixture

from puller.controller import Puller
from puller.queries import Queries


JSON_DATA = [
    {"date":1,"price":33,"type":"sell","amount":0.011364,"tid":"1"},
    {"date":2,"price":44,"type":"buy","amount":0.5,"tid":"2"},
]
TICKER_ID = 0
DATA_TO_INSERT = [['1', 1, 33, 0.011364, TICKER_ID], ['2', 2, 44, 0.5, TICKER_ID]]
TICKERS = ['btcpln']


class MockResp():
    def json(self):
        return JSON_DATA


class EmptyMockResp():
    def json(self):
        return False


def test_puller(mocker: MockerFixture) -> None:
    mocker.patch('puller.queries.Queries.select_id_by_ticker', return_value=[TICKER_ID])
    mocker.patch('puller.queries.Queries.select_last_transaction_tid', return_value=[0])
    mocker.patch('requests.Session.get', side_effect=[MockResp(), EmptyMockResp()])

    puller = Puller()
    puller.TICKERS = TICKERS
    queries = Queries(mocker.Mock())
    spy = mocker.spy(queries, 'insert_trade')

    puller._pull_trades(queries)
    spy.assert_called_once_with(bulk_values=DATA_TO_INSERT)
