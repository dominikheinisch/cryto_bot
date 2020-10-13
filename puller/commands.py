import click
import time

from database import db
from puller.controller import run


@click.group()
def commands_group():
    pass


@commands_group.command()
def init_db():
    db.init_db()


@commands_group.command()
def fetch_btc_pln():
    with db.get_db() as _db:
        start_time = time.time()
        btcpln = _db.execute(
            'SELECT * FROM trades WHERE ticker_id = (?) ORDER BY date_ DESC LIMIT(10000)',
            [1]
        ).fetchall()
        print(time.time() - start_time)
        for trade in btcpln[::1000]:
            print(trade)


@commands_group.command()
def run_puller():
    run()