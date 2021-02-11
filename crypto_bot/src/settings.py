from os import path


class Database:
    DB_DATA_DIR = path.join('/app', 'db-data')
    PATH = path.join(DB_DATA_DIR, 'db.sqlite3')
    SCHEMA_PATH = path.join(DB_DATA_DIR, 'schema.sql')


class Paths:
    LOGGER = path.join('/app', 'logs', 'crypto_bot.log')
    PREPROCESSOR = path.join('/app', 'preprocessed-data')


TICKERS = ['btcpln', 'lskpln', 'bccpln', 'ltcpln', 'omgpln', 'xrppln', 'ethpln', 'btgpln', 'bsvpln', 'trxpln', ]
