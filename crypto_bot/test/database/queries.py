class TestQueries():
    def __init__(self, conn):
        self._conn = conn

    def select_all_id_ticker(self):
        return self._conn.execute(
            query='SELECT id, ticker FROM tickers ORDER BY id ASC',
            func=lambda cursor: cursor.fetchall,
        )

    def select_max_tid(self, ticker_id):
        return self._conn.execute(
            query='SELECT MAX(tid) FROM trades WHERE ticker_id = %s',
            vars=(ticker_id,),
            func=lambda cursor: cursor.fetchone,
        )[0]

    def select_count(self, ticker_id):
        return self._conn.execute(
            query='SELECT COUNT(*) FROM trades WHERE ticker_id =%s',
            vars=(ticker_id,),
            func=lambda cursor: cursor.fetchone,
        )[0]
