from src.database.db import get_db
from src.database.queries import Queries as PgQueries
from src.puller.queries import Queries as SqliteQueries
from src.utils.func import named_timer


class Migration:
    _LIMIT = 100000

    def sqlite_to_postgres(self):
        with get_db() as conn:
            self._sqlite_queries = SqliteQueries(conn)
            self._pg_queries = PgQueries()
            ids_tickers = self._sqlite_queries.select_all_from_tickers()
            self._pg_queries.insert_tickers(ids_tickers)
            self._migrate_trades(ids_tickers=ids_tickers)

    def _migrate_trades(self, ids_tickers):
        for id, ticker in ids_tickers:
            print(id, ticker)
            self._migrate_trades_batches(ticker=ticker)

    def _migrate_trades_batches(self, ticker):
        offset_generator = self._offset_generator()
        ticker_trades = True
        while ticker_trades:
            offset = next(offset_generator)
            print(f'for {ticker}, limit: {self._LIMIT}, offset: {offset}')
            ticker_trades = self._sqlite_queries.select_all_by_ticker_limited(ticker, limit=self._LIMIT, offset=offset)
            self._insert_trades(trades=[trade[1:] for trade in ticker_trades])

    def _offset_generator(self):
        offset = 0
        while True:
            yield offset
            offset += self._LIMIT

    def _insert_trades(self, trades):
        named_timer(log_name='insert_trades')(func=self._pg_queries.insert_trades)(bulk_values=trades)
