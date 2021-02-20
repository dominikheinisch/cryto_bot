import pandas as pd

from src.database.model import TRADE_FIELDS


class TradeFilter:
    _TRADE_HOUR_UTC = 16
    _BATCH_THRESHOLD = 24
    __MIN_HOUR = -1
    __MAX_HOUR = 24
    __ACCEPTED_BATCH_THRESHOLD = [1, 2, 3, 4, 6, 8, 12, 24]

    def __init__(self, threshold_hour_utc=None, batch_threshold=None):
        self.__threshold_hour = threshold_hour_utc if threshold_hour_utc else self._TRADE_HOUR_UTC
        self.__batch_threshold = batch_threshold if batch_threshold else self._BATCH_THRESHOLD

    def filter(self, trades):
        self.assert_input()
        df = pd.DataFrame(trades, columns=TRADE_FIELDS)
        df['created_at'] = self.__align_datetime(df)
        df['category'] = self.__create_category(df)
        df['created_at'] = df['created_at'].dt.floor('d')
        return df.groupby(['created_at', 'category']).first()['price'].values

    def assert_input(self):
        assert self.__MIN_HOUR < self.__threshold_hour <= self.__MAX_HOUR
        assert isinstance(self.__batch_threshold, int)
        assert self.__batch_threshold in self.__ACCEPTED_BATCH_THRESHOLD

    def __create_category(self, df):
        return pd.cut(
            x=df['created_at'].dt.hour,
            bins=list(range(self.__MIN_HOUR, self.__MAX_HOUR, self.__batch_threshold)),
            labels=range(self.__MAX_HOUR // self.__batch_threshold)
        ).astype(int)

    def __align_datetime(self, df):
        threshold = pd.to_timedelta(self.__threshold_hour, unit='h')
        return pd.to_datetime(df['created_at'], unit='s') - threshold
