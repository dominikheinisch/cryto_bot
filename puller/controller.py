import requests
import time
from datetime import datetime
from typing import List

from database import db


def get_data(ticker, category, since):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{ticker}/{category}.json?since={since}')
    return data.json()


def get_trade_data(row):
    return row['tid'], row['date'], row['price'], row['amount']


def process_ticker(db, ticker):
    def get_ticker_id(db):
        return db.execute(
            'SELECT id FROM tickers WHERE ticker = (?)',
            [ticker]
        ).fetchone()
    ids = get_ticker_id(db)
    if not ids:
        db.execute(
            'INSERT INTO tickers (ticker, is_synthetic) VALUES (?, ?)',
            [ticker, 0]
        )
        db.commit()
        ids = get_ticker_id(db)
    return ids[0]


def process_data(db, data, ticker_id):
    row = get_trade_data(data[0])
    print(*row, datetime.fromtimestamp(row[1]).strftime("%d.%m.%Y %I:%M:%S"), ticker_id)
    start_time = time.time()
    db.executemany(
        'INSERT INTO trades (tid, date_, price, amount, ticker_id) VALUES (?, ?, ?, ?, ?)',
        [[*get_trade_data(row), ticker_id] for row in data]
    )
    db.commit()
    print('commit', time.time() - start_time)


def get_last_transaction_tid(db, ticker_id):
    id = db.execute(
        'SELECT MAX(tid) FROM trades WHERE ticker_id = (?)',
        [ticker_id]
    ).fetchone()
    return id[0] if id[0] else -1


def pull_trades(db, ticker: str, TRADES_SIZE: int=50):
    ticker_id = process_ticker(db, ticker=ticker)
    tid_since = get_last_transaction_tid(db, ticker_id)

    start_time = time.time()
    data = get_data(ticker=ticker, category='trades', since=tid_since)
    while(data):
        process_data(db, data, ticker_id)
        tid_since += TRADES_SIZE
        print(time.time() - start_time)
        data = get_data(ticker=ticker, category='trades', since=tid_since)


def pull_all_trades(db, tickers: List[str]=['btcpln', 'lskpln', 'bccpln', 'ltcpln', 'omgpln', 'xrppln', 'ethpln', 'btgpln']):
    [pull_trades(db, ticker) for ticker in tickers]


def run():
    with db.get_db() as _db:
        while(True):
            try:
                pull_all_trades(_db)
                time.sleep(30)
            except Exception as e:
                print(e)