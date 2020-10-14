import requests
import time
from datetime import datetime

from puller.queries import Queries
from database import db


class Puller:
    TICKERS = ['btcpln', 'lskpln', 'bccpln', 'ltcpln', 'omgpln', 'xrppln', 'ethpln', 'btgpln', 'bsvpln', 'trxpln',]

    def __init__(self):
        self.queries = None

    def run(self):
        with db.get_db() as _db:
            self.queries = Queries(_db)
            while(True):
                try:
                    self.pull_trades()
                    time.sleep(30)
                except Exception as e:
                    print(e)

    def pull_trades(self):
        [TickerTrades(self.queries, ticker).pull_trades() for ticker in self.TICKERS]


class TickerTrades:
    TRADES_SIZE = 50

    def __init__(self, queries: Queries, ticker: str):
        self.queries = queries
        self.ticker = ticker
        self.ticker_id = self.process_ticker(ticker)
        self.tid_since = self.get_last_transaction_tid()
        self.data = None

    def process_ticker(self, ticker) -> int:
        ids = self.queries.select_id_by_ticker(ticker)
        if not ids:
            self.queries.insert_ticker(ticker)
            ids = self.queries.select_id_by_ticker(ticker)
        return ids[0]

    def get_last_transaction_tid(self) -> int:
        id = self.queries.select_last_transaction_tid(self.ticker_id)
        return id[0] if id[0] else -1

    def pull_trades(self):
        while (self.get_data()):
            self.process_data(self.data)
            self.tid_since += self.TRADES_SIZE

    def get_data(self, category='trades'):
        session = requests.Session()
        data = session.get(f'https://bitbay.net/API/Public/{self.ticker}/{category}.json?since={self.tid_since}')
        self.data = data.json()
        return self.data

    def process_data(self, data):
        def get_trade_data(row):
            return row['tid'], row['date'], row['price'], row['amount']
        row = get_trade_data(data[0])
        print(self.ticker, datetime.fromtimestamp(row[1]).strftime("%d.%m.%Y %I:%M:%S"), data[0])
        self.queries.insert_trade(bulk_values=[[*get_trade_data(row), self.ticker_id] for row in data])
