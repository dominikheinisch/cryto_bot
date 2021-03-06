import pandas as pd
from time import sleep
from pybitbay import BitBayAPI

import src.settings as settings
from src.database.queries import Queries
from src.utils.logger import get_logger


class Puller:
    def run(self, tickers=settings.TICKERS):
        queries = Queries()
        while True:
            self._pull_trades(queries, tickers)
            sleep(10)

    def _pull_trades(self, queries, tickers):
        for ticker in tickers:
            TickerTrades(queries, ticker).pull_trades()


class TickerTrades:
    def __init__(self, queries: Queries, ticker: str):
        self._queries = queries
        self._logger = get_logger()
        self._ticker = ticker
        self.ticker_id = None

    def pull_trades(self):
        self.ticker_id = self._process_ticker()
        tid_since = self._get_last_transaction_tid()
        for df in BitBayAPI().get_all_trades(ticker=self._ticker, since=tid_since):
            self._log(df.loc[0])
            bulk = self._prepare_data_to_insert(df)
            self._queries.insert_trades(bulk_values=bulk)

    def _process_ticker(self) -> int:
        ids = self._queries.select_id_by_ticker(self._ticker)
        if not ids:
            self._queries.insert_ticker(self._ticker)
            ids = self._queries.select_id_by_ticker(self._ticker)
        return ids[0]

    def _log(self, row):
        self._logger.info(', '.join(map(str, [self._ticker, pd.to_datetime(row['date'], unit='s'), row.to_dict()])))
        print(self._ticker, pd.to_datetime(row['date'], unit='s'), row.to_dict())

    def _get_last_transaction_tid(self) -> int:
        id = self._queries.select_last_transaction_tid(self.ticker_id)
        return id[0] if id[0] else -1

    def _prepare_data_to_insert(self, df):
        bulk = df[['tid', 'date', 'price', 'amount']]
        bulk.insert(loc=1, column='ticker_id', value=self.ticker_id)
        bulk.rename(columns={'date': 'created_at'}, inplace=True)
        return bulk.values.tolist()
