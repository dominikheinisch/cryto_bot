import pandas as pd
from pytest_mock import MockerFixture

from crypto_bot.puller.controller import Puller
from crypto_bot.puller.queries import Queries

TICKER_ID = 5
TICKERS = ['btcpln']
COLUMNS = ['date', 'price', 'type', 'amount', 'tid']
DATA = [
    {"date": 1396094988, "price": 4500, "type": "buy", "amount": 0.0129, "tid": "0"},
    {"date": 1396096603, "price": 4400, "type": "sell", "amount": 0.011364, "tid": "1"},
]
MOCK_DATA = pd.DataFrame(
    data=[[row[col] for col in COLUMNS] for row in DATA],
    columns=COLUMNS
)
EXPECTED = [
    [row['tid'], row['date'], row['price'], row['amount'], TICKER_ID] for row in DATA
]


def test_controller(mocker: MockerFixture):
    mocker.patch('crypto_bot.puller.queries.Queries.select_id_by_ticker', return_value=[TICKER_ID])
    mocker.patch('crypto_bot.puller.queries.Queries.select_last_transaction_tid', return_value=[-1])
    mocker.patch('crypto_bot.puller.bitbay_api.BitbayApi.get_all_trades', side_effect=[[MOCK_DATA]])

    queries = Queries(mocker.Mock())
    spy = mocker.spy(queries, 'insert_trade')

    Puller()._pull_trades(queries, tickers=TICKERS)
    spy.assert_called_once_with(bulk_values=EXPECTED)
