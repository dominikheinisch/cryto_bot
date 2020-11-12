import numpy as np
import pickle
from datetime import datetime, timedelta

from database import db
from utils.func import named_timer, ticker_to_path
from puller.queries import Queries


class TradeFilter:
    DAY_TO_SEC = 24 * 3600
    DATE_0 = datetime(1970, 1, 1)
    DATE_PATTERN = '%d.%m.%Y'
    TRADE_HOUR = timedelta(hours=16)

    def __init__(self, trades, sample_size=None):
        self.__trades = trades
        self.__timestamp_sec = None
        self.__sample_size = sample_size if sample_size else self.DAY_TO_SEC

    def filter(self):
        self.__timestamp_sec = self.__get_first_timestamp(self.__trades[0].datetime)
        return self.__get_trade_per_batch()

    def __get_first_timestamp(self, date) -> int:
        date_from_stamp = datetime.fromtimestamp(date).strftime(self.DATE_PATTERN)
        timestamp_date = datetime.strptime(date_from_stamp, self.DATE_PATTERN) + self.TRADE_HOUR
        return (timestamp_date - self.DATE_0).total_seconds()

    def __get_trade_per_batch(self):
        return list(filter(lambda trade: self.__is_first_in_batch(trade.datetime), self.__trades))

    def __is_first_in_batch(self, datetime: int) -> bool:
        if datetime > self.__timestamp_sec:
            self.__timestamp_sec += self.__sample_size
            return True
        return False


class Preparator:
    SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    def __init__(self):
        self.__trades = None

    @named_timer('data set preparation')
    def prepare(self, ticker):
        with db.get_db() as _db:
            queries = Queries(_db)
            self.__trades = queries.select_all_by_ticker(ticker)
            filtered_trades = TradeFilter(self.__trades).filter()
            prices = self.__filter_prices(filtered_trades)
            data_set = self.__prepare_data_set(prices)
            self.__save(data_set, ticker)

    def __filter_prices(self, filtered_trades):
        return np.asarray([trade.price for trade in filtered_trades])

    def __prepare_data_set(self, prices) -> dict:
        samples_begin = max(self.SEQUENCE) + 1
        y = prices[samples_begin:]
        N = y.shape[0]
        prices = prices[::-1]
        seq = np.asarray(self.SEQUENCE)
        x = np.zeros(shape=(N, len(seq)))
        for i in range(N):
            x[i] = prices[seq]
            seq += 1
        x = np.flip(x, axis=0)
        max_val, x, y = self.__normalize(x, y)
        return {'x': x, 'y': y, 'max_val': max_val}

    def __normalize(self, x, y):
        max_val = np.amax(x)
        x /= max_val
        y /= max_val
        return max_val, x, y

    def __save(self, model_data, ticker):
        with open(ticker_to_path(ticker), 'wb') as pickle_file:
            pickle.dump(model_data, pickle_file)

    def __load(self, ticker):
        with open(ticker_to_path(ticker), 'rb') as pickle_file:
            model_data = pickle.load(pickle_file)
            print(model_data)
