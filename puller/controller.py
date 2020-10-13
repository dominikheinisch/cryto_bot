import requests
import time
from datetime import datetime
from typing import List

import puller.queries as queries
from database import db


def get_data(ticker, category, since):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{ticker}/{category}.json?since={since}')
    return data.json()


def get_trade_data(row):
    return row['tid'], row['date'], row['price'], row['amount']


def process_ticker(db, ticker):
    ids = queries.select_id_by_ticker(db, ticker)
    if not ids:
        queries.insert_ticker(db, ticker)
        ids = queries.select_id_by_ticker(db, ticker)
    return ids[0]


def process_data(db, data, ticker_id):
    row = get_trade_data(data[0])
    print(*row, datetime.fromtimestamp(row[1]).strftime("%d.%m.%Y %I:%M:%S"), ticker_id)
    start_time = time.time()
    queries.insert_trade(db, bulk_values=[[*get_trade_data(row), ticker_id] for row in data])
    print('commit', time.time() - start_time)


def get_last_transaction_tid(db, ticker_id):
    id = queries.select_last_transaction_tid(db, ticker_id)
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


def pull_all_trades(db, tickers: List[str]=[
        'btcpln', 'lskpln', 'bccpln', 'ltcpln', 'omgpln', 'xrppln', 'ethpln', 'btgpln', 'trxpln',]):
    [pull_trades(db, ticker) for ticker in tickers]


def run():
    with db.get_db() as _db:
        while(True):
            try:
                pull_all_trades(_db)
                time.sleep(30)
            except Exception as e:
                print(e)