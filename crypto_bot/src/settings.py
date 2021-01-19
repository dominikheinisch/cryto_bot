from os import path


DB_DATA_DIR = path.join("/app", "db-data")


class Database:
    PATH = path.join(DB_DATA_DIR, 'db.sqlite3')
    SCHEMA_PATH = path.join(DB_DATA_DIR, 'schema.sql')


class Datasets:
    DIR = path.join(DB_DATA_DIR, 'datasets')


TICKERS = ['btcpln', 'lskpln', 'bccpln', 'ltcpln', 'omgpln', 'xrppln', 'ethpln', 'btgpln', 'bsvpln', 'trxpln', ]
