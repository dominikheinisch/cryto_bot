from os import path


BASE_DIR = path.dirname(path.abspath(__file__))


class Database:
    DIR = path.join(BASE_DIR, 'database')
    PATH = path.join(DIR, 'db.sqlite3')
    SCHEMA_PATH = path.join(DIR, 'schema.sql')


class Datasets:
    DIR = path.join(BASE_DIR, 'datasets')


TICKERS = ['btcpln', 'lskpln', 'bccpln', 'ltcpln', 'omgpln', 'xrppln', 'ethpln', 'btgpln', 'bsvpln', 'trxpln', ]
