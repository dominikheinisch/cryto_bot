from datetime import datetime, timezone
from collections import namedtuple

from src.preprocessor.preprocessor import TradeFilter
from src.database.model import Trade


class TestTradeFilter():
    def test_one(self):
        run(input=[TRADE_1.Trade], result=[TRADE_1.price])

    def test_two_after_threshold(self):
        run(input=[TRADE_1.Trade, TRADE_2.Trade], result=[TRADE_1.price])

    def test_two_for_different_days(self):
        run(input=[TRADE_1.Trade, TRADE_3.Trade], result=[TRADE_1.price, TRADE_3.price])

    def test_two_for_different_days_mixed_time(self):
        run(input=[TRADE_1.Trade, TRADE_4.Trade], result=[TRADE_1.price, TRADE_4.price])

    def test_threshold_split(self):
        run(input=[TRADE_0.Trade, TRADE_1.Trade], result=[TRADE_0.price, TRADE_1.price])

    def test_not_sorted(self):
        run(input=[TRADE_2.Trade, TRADE_1.Trade], result=[TRADE_2.price])

    def test_many_days(self):
        run(input=[TRADE_0.Trade, TRADE_1.Trade, TRADE_2.Trade, TRADE_3.Trade, TRADE_4.Trade],
            result=[TRADE_0.price, TRADE_1.price, TRADE_3.price, TRADE_4.price])

    def test_batch_threshold(self):
        run(input=[TRADE_4.Trade, TRADE_5.Trade, TRADE_6.Trade, TRADE_7.Trade, TRADE_8.Trade],
            result=[TRADE_4.price, TRADE_5.price, TRADE_8.price])


def run(input, result):
    assert all(
        TradeFilter(
            threshold_hour_utc=THRESHOLD_HOUR,
            batch_threshold=BATCH_THRESHOLD,
        ).filter(input) == result)


def get_fake_trade(dtime: str, price: float):
    return TradePrice(Trade(id=0, tid=0, ticker_id=0, datetime=datetime_from_str(dtime), price=price, amount=0), price)


def datetime_from_str(dtime: str) -> int:
    return datetime.timestamp(datetime.strptime(dtime, ('%Y-%m-%d %H:%M:%S')).replace(tzinfo=timezone.utc))


TradePrice = namedtuple('TradePrice', ['Trade', 'price'])
THRESHOLD_HOUR = 17
BATCH_THRESHOLD = 4
TRADE_0 = get_fake_trade('2020-01-01 16:59:59', 0.5)
TRADE_1 = get_fake_trade('2020-01-01 17:00:01', 1.5)
TRADE_2 = get_fake_trade('2020-01-01 17:00:02', 2.33)
TRADE_3 = get_fake_trade('2020-01-03 17:00:02', 3.01)
TRADE_4 = get_fake_trade('2020-01-04 13:00:02', 4.0)
TRADE_5 = get_fake_trade('2020-01-04 17:00:02', 4.1)
TRADE_6 = get_fake_trade('2020-01-04 18:00:02', 4.2)
TRADE_7 = get_fake_trade('2020-01-04 20:59:59', 4.3)
TRADE_8 = get_fake_trade('2020-01-04 21:00:01', 4.4)
