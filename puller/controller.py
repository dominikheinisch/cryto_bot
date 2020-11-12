from datetime import datetime
from requests import Session
from time import sleep

import settings
from puller.queries import Queries
from database import db


class Puller:
    def run(self):
        with db.get_db() as _db:
            queries = Queries(_db)
            while True:
                try:
                    self._pull_trades(queries)
                    sleep(30)
                except Exception as e:
                    print(e)

    def _pull_trades(self, queries):
        for ticker in settings.TICKERS:
            TickerTrades(queries, ticker).pull_trades()


class TickerTrades:
    TRADES_SIZE = 50

    def __init__(self, queries: Queries, ticker: str):
        self._queries = queries
        self._ticker = ticker
        self.ticker_id = None

    def pull_trades(self):
        self.ticker_id = self._process_ticker()
        tid_since = self._get_last_transaction_tid()
        data = self._pull_trades_batch(tid_since)
        while data:
            self._process(data)
            tid_since += self.TRADES_SIZE
            data = self._pull_trades_batch(tid_since)

    def _process_ticker(self) -> int:
        ids = self._queries.select_id_by_ticker(self._ticker)
        if not ids:
            self._queries.insert_ticker(self._ticker)
            ids = self._queries.select_id_by_ticker(self._ticker)
        return ids[0]

    def _get_last_transaction_tid(self) -> int:
        id = self._queries.select_last_transaction_tid(self.ticker_id)
        return id[0] if id[0] else -1

    def _pull_trades_batch(self, tid_since, category='trades'):
        data = Session().get(f'https://bitbay.net/API/Public/{self._ticker}/{category}.json?since={tid_since}')
        return data.json()

    def _process(self, data):
        def get_trade_data(row):
            return row['tid'], row['date'], row['price'], row['amount']
        print(self._ticker, datetime.fromtimestamp(data[0]['date']).strftime("%d.%m.%Y %I:%M:%S"), data[0])
        self._queries.insert_trade(bulk_values=[[*get_trade_data(row), self.ticker_id] for row in data])
