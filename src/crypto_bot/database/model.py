from collections import namedtuple

TRADE_FIELDS = ['id', 'tid', 'ticker_id', 'datetime', 'price', 'amount']
Trade = namedtuple('Trade', TRADE_FIELDS)
