from src.database.model import Trade
from src.utils.func import named_timer


class Queries:
    def __init__(self, db):
        self.db = db

    def select_id_by_ticker(self, ticker):
        return self.db.execute(
            'SELECT id FROM tickers WHERE ticker = (?)',
            [ticker]
        ).fetchone()

    def select_all_from_tickers(self):
        return self.db.execute(
            'SELECT id, ticker FROM tickers',
        ).fetchall()

    def insert_ticker(self, ticker, is_synthetic=0):
        self.db.execute(
            'INSERT INTO tickers (ticker, is_synthetic) VALUES (?, ?)',
            [ticker, is_synthetic]
        )
        self.db.commit()

    def insert_trades(self, bulk_values):
        self.db.executemany(
            'INSERT INTO trades (tid, ticker_id, date_, price, amount) VALUES (?, ?, ?, ?, ?)',
            [[*values] for values in bulk_values]
        )
        self.db.commit()

    def select_last_transaction_tid(self, ticker_id):
        return self.db.execute(
            'SELECT MAX(tid) FROM trades WHERE ticker_id = (?)',
            [ticker_id]
        ).fetchone()

    @named_timer('fetching all by ticker')
    def select_all_by_ticker(self, ticker):
        id = self.select_id_by_ticker(ticker)
        trades = self.db.execute(
            'SELECT id, tid, ticker_id, date_, price, amount '
            'FROM trades '
            'WHERE ticker_id = (?) '
            'ORDER BY tid ASC',
            [id[0]]
        ).fetchall()
        return [Trade(*row) for row in trades]

    @named_timer('fetching all by ticker')
    def select_all_by_ticker_limited(self, ticker, limit, offset):
        id = self.select_id_by_ticker(ticker)
        trades = self.db.execute(
            'SELECT id, tid, ticker_id, date_, price, amount '
            'FROM trades '
            'WHERE ticker_id = (?) '
            'ORDER BY tid ASC '
            'LIMIT (?) '
            'OFFSET (?) ',
            [id[0], limit, offset]
        ).fetchall()
        return [Trade(*row) for row in trades]
