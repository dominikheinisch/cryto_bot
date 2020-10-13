def select_id_by_ticker(db, ticker):
    return db.execute(
        'SELECT id FROM tickers WHERE ticker = (?)',
        [ticker]
    ).fetchone()


def insert_ticker(db, ticker, is_synthetic=0):
    db.execute(
        'INSERT INTO tickers (ticker, is_synthetic) VALUES (?, ?)',
        [ticker, is_synthetic]
    )
    db.commit()


def insert_trade(db, bulk_values):
    db.executemany(
        'INSERT INTO trades (tid, date_, price, amount, ticker_id) VALUES (?, ?, ?, ?, ?)',
        [[*values] for values in bulk_values]
    )
    db.commit()


def select_last_transaction_tid(db, ticker_id):
    return db.execute(
        'SELECT MAX(tid) FROM trades WHERE ticker_id = (?)',
        [ticker_id]
    ).fetchone()