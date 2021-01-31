from collections import namedtuple

TRADE_FIELDS = ['id', 'tid', 'ticker_id', 'created_at', 'price', 'amount']
Trade = namedtuple('Trade', TRADE_FIELDS)
