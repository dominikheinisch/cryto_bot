from src.database.model import Trade
from src.database.pg_connector import PgConnector
from src.utils.func import named_timer


class Queries:
    def __init__(self):
        self.conn = PgConnector()

    def select_id_by_ticker(self, ticker):
        return self.conn.execute(
            query='SELECT id FROM tickers WHERE ticker = %s',
            vars=(ticker,),
            func=lambda cursor: cursor.fetchone,
        )

    def insert_tickers(self, bulk_values):
        return self.conn.executemany(
            query='INSERT INTO tickers (id, ticker) VALUES (%s, %s)',
            vars_list=([*values] for values in bulk_values),
        )

    def insert_ticker(self, ticker, is_synthetic=0):
        self.conn.execute(
            query='INSERT INTO tickers (ticker) VALUES (%s)',
            vars=(ticker,),
        )

    def insert_trades(self, bulk_values):
        self.conn.executemany(
            query='INSERT INTO trades (tid, ticker_id, created_at, price, amount) VALUES (%s, %s, %s, %s ,%s)',
            vars_list=([*values] for values in bulk_values),
        )

    def select_last_transaction_tid(self, ticker_id):
        return self.conn.execute(
            query='SELECT MAX(tid) FROM trades WHERE ticker_id = %s',
            vars=(ticker_id,),
            func=lambda cursor: cursor.fetchone,
        )

    @named_timer('fetching all by ticker')
    def select_all_by_ticker(self, ticker):
        id = self.select_id_by_ticker(ticker)
        trades = self.conn.execute(
            query='SELECT id, tid, ticker_id, created_at, price, amount '
                  'FROM trades '
                  'WHERE ticker_id = %s '
                  'ORDER BY tid ASC ',
            vars=(id[0],),
            func=lambda cursor: cursor.fetchall,
        )
        return [Trade(*row) for row in trades]
