import numpy as np
from datetime import datetime, timedelta


class TradeFilter:
    DAY_TO_SEC = 24 * 3600
    DATE_0 = datetime(1970, 1, 1)
    DATE_PATTERN = '%Y-%m-%d'
    TRADE_HOUR_UTC = 16

    def __init__(self, trades, threshold_hour_utc=None, sample_size=None):
        self.__trades = trades
        self.__timestamp_sec = None
        self.__threshold_hour = timedelta(hours=threshold_hour_utc if threshold_hour_utc else self.TRADE_HOUR_UTC)
        self.__sample_size = sample_size if sample_size else self.DAY_TO_SEC

    def filter(self):
        self.__timestamp_sec = self.__get_first_timestamp(self.__trades[0].datetime)
        return self.__get_price_per_batch()

    def __get_first_timestamp(self, datetime_: int) -> int:
        date_from_stamp = datetime.fromtimestamp(datetime_).strftime(self.DATE_PATTERN)
        timestamp_date = datetime.strptime(date_from_stamp, self.DATE_PATTERN) + self.__threshold_hour
        return (timestamp_date - self.DATE_0).total_seconds()

    def __get_price_per_batch(self):
        return np.asarray([trade.price for trade in self.__trades if self.__is_first_in_batch(trade.datetime)])

    def __is_first_in_batch(self, datetime_: int) -> bool:
        if datetime_ >= self.__timestamp_sec:
            self.__timestamp_sec += self.__sample_size
            return True
        return False
