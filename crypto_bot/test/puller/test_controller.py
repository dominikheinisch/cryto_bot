import pandas as pd
from pytest_mock import MockerFixture

from src.puller.controller import Puller
from src.database.queries import Queries

TICKER_ID = 5
TICKERS = ['btcpln']
JSON_DATA = [
    {"date": 1396094988, "price": 4500, "type": "buy", "amount": 0.0129, "tid": "0"},
    {"date": 1396096603, "price": 4400, "type": "sell", "amount": 0.011364, "tid": "1"},
]
COLUMNS = JSON_DATA[0].keys()
MOCKED_DF = pd.DataFrame(
    data=JSON_DATA,
    columns=COLUMNS
)
EXPECTED = [
    [row['tid'], TICKER_ID, row['date'], row['price'], row['amount']] for row in JSON_DATA
]


def test_controller(mocker: MockerFixture):
    mocker.patch('src.database.pg_connector.PgConnector.__init__', return_value=None)
    mocker.patch('src.database.queries.Queries.select_id_by_ticker', return_value=[TICKER_ID])
    mocker.patch('src.database.queries.Queries.select_last_transaction_tid', return_value=[-1])
    mocker.patch('pybitbay.BitBayAPI.get_all_trades', side_effect=[[MOCKED_DF]])

    queries = Queries()
    queries.conn = mocker.Mock()
    spy = mocker.spy(queries, 'insert_trades')

    Puller()._pull_trades(queries, tickers=TICKERS)
    spy.assert_called_once_with(bulk_values=EXPECTED)
