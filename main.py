import click
import requests
import time
from datetime import datetime

from database import db


def get_data(symbol, category, since):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{symbol}/{category}.json?since={since}')
    return data.json(), symbol

def get_trades(symbol, since):
    return get_data(symbol=symbol, category='trades', since=since)


def trade_data(row):
    tid = row['tid']
    date = row['date']
    price = row['price']
    amount = row['amount']
    return tid, date, price, amount


def process_ticker(db, ticker):
    def get_ticker_id(db):
        return db.execute(
            'SELECT id FROM tickers WHERE ticker = (?)',
            [ticker]
        ).fetchone()
    ids = get_ticker_id(db)
    if ids:
        return ids[0]
    else:
        db.execute(
            'INSERT INTO tickers (ticker, is_synthetic) VALUES (?, ?)',
            [ticker, 0]
        )
        db.commit()
        return get_ticker_id(db)[0]


def process_data(db, data, ticker_id):
    row = trade_data(data[0])
    print(*row, datetime.fromtimestamp(row[2]).strftime("%d.%m.%Y %I:%M:%S"), ticker_id)
    start_time = time.time()
    db.executemany(
        'INSERT INTO trades (tid, date_, price, amount, ticker_id) VALUES (?, ?, ?, ?, ?)',
        [[*trade_data(row), ticker_id] for row in data]
    )
    db.commit()
    print('commit', time.time() - start_time)

def get_last_transaction_tid(db, ticker_id):
    id = db.execute(
        'SELECT MAX(tid) FROM trades WHERE ticker_id = (?)',
        [ticker_id]
    ).fetchone()
    if id[0]:
        return id[0]
    else:
        return -1


def pull_trades(db, symbol):
    TRADES_SIZE = 50
    ticker_id = process_ticker(db, ticker=symbol)
    tid_since = get_last_transaction_tid(db, ticker_id)
    is_empty = False
    start_time = time.time()
    while(not is_empty):
        data, symbol = get_data(symbol=symbol, category='trades', since=tid_since)
        process_data(db, data, ticker_id)
        is_empty = not len(data)
        tid_since += TRADES_SIZE
        print(time.time() - start_time)

def pull_all_trades(db, symbols=['btcpln', 'lskpln']):
    [pull_trades(db, symbol) for symbol in symbols]


@click.group()
def cli():
  pass


@cli.command()
def init_db():
    db.init_db()


@cli.command()
def run_puller():
    with db.get_db() as _db:
        def run():
            while(True):
                try:
                    pull_all_trades(_db)
                    time.sleep(30)
                except:
                    run()
        run()


if __name__ == '__main__':
    cli()
