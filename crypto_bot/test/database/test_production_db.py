import pytest


@pytest.mark.slow
class TestProductionDB:
    def test_database_consistency(self, production_db_conn):
        queries = Queries(production_db_conn)
        for ticker, count, max_tid, ticker_id in queries.select_ticker_count_max_tid():
            print(f'ticker={ticker}, count={count}, max_tid={max_tid}, ticker_id={max_tid}')
            assert count == max_tid + 1


class Queries():
    def __init__(self, conn):
        self._conn = conn

    def select_ticker_count_max_tid(self):
        return self._conn.execute(
            query='SELECT ticker, cnt, max_tid, ticker_id '
                  'FROM tickers INNER JOIN ('
                  '  SELECT ticker_id, COUNT(*) AS cnt, MAX(tid) AS max_tid '
                  '  FROM trades '
                  '  GROUP BY ticker_id '
                  ') AS grouped_trades '
                  'ON tickers.id = grouped_trades.ticker_id',
            func=lambda cursor: cursor.fetchall,
        )
