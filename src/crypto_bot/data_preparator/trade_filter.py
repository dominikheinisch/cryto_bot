import pandas as pd

from crypto_bot.database.model import TRADE_FIELDS


class TradeFilter:
    TRADE_HOUR_UTC = 16

    def __init__(self, threshold_hour_utc=None):
        self.__threshold_hour = threshold_hour_utc if threshold_hour_utc else self.TRADE_HOUR_UTC

    def filter(self, trades):
        threshold = pd.to_timedelta(self.__threshold_hour, unit='h')
        df = pd.DataFrame(trades, columns=TRADE_FIELDS)
        df['datetime'] = (pd.to_datetime(df['datetime'], unit='s') - threshold) \
            .dt.floor('d')
        return df.groupby('datetime').first()['price'].values
