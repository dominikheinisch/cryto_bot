class TestQueries():
    def select_all_id_ticker(self, db):
        return db.execute(
            'SELECT id, ticker FROM tickers ORDER BY id ASC',
        ).fetchall()

    def select_max_tid(self, db, ticker_id):
        return db.execute(
            'SELECT MAX(tid) FROM trades WHERE ticker_id = (?)',
            [ticker_id],
        ).fetchone()[0]

    def select_count(self, db, ticker_id):
        return db.execute(
            'SELECT COUNT(*) FROM trades WHERE ticker_id = (?)',
            [ticker_id],
        ).fetchone()[0]
