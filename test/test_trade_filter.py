from datetime import datetime, timezone

from crypto_bot.data_preparator.preparator import TradeFilter
from crypto_bot.database.model import Trade


class TestTradeFilter():
    def test_one(self):
        run(input=[TRADE_1], result=[TRADE_1])

    def test_one_ommit_due_to_threshold(self):
        run(input=[TRADE_0], result=[])

    def test_two_in_same_range(self):
        run(input=[TRADE_1, TRADE_2], result=[TRADE_1])

    def test_two_for_different_days(self):
        run(input=[TRADE_1, TRADE_3], result=[TRADE_1, TRADE_3])

    def test_two_for_different_days_mixed_time(self):
        run(input=[TRADE_1, TRADE_4], result=[TRADE_1, TRADE_4])

    def test_ommit_first(self):
        run(input=[TRADE_0, TRADE_1], result=[TRADE_1])

    def test_not_sorted(self):
        run(input=[TRADE_2, TRADE_1], result=[TRADE_2])


def run(input, result):
    assert TradeFilter(input, threshold_hour_utc=THRESHOLD_HOUR).filter() == result


def get_fake_trade(id: int, dtime: str):
    return Trade(id=id, tid=id, ticker_id=0, datetime=datetime_from_str(dtime), price=0, amount=0)


def datetime_from_str(dtime: str) -> int:
    return datetime.timestamp(datetime.strptime(dtime, ('%Y-%m-%d %H:%M:%S')).replace(tzinfo=timezone.utc))


THRESHOLD_HOUR = 17
TRADE_0 = get_fake_trade(0, '2020-01-01 16:59:59')
TRADE_1 = get_fake_trade(1, '2020-01-01 17:00:01')
TRADE_2 = get_fake_trade(2, '2020-01-01 17:00:02')
TRADE_3 = get_fake_trade(3, '2020-01-03 17:00:02')
TRADE_4 = get_fake_trade(4, '2020-01-04 13:00:02')
