import numpy as np
import pickle

from crypto_bot.database import db
from crypto_bot.utils.func import named_timer, ticker_to_path
from crypto_bot.puller.queries import Queries
from crypto_bot.data_preparator.trade_filter import TradeFilter


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
