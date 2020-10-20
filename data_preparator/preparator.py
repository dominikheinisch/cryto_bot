import numpy as np
import pickle
import time
from datetime import datetime, timedelta

from database import db
from utils.func import ticker_to_path
from puller.queries import Queries


class Preparator:
    BATCH_TO_SEC = 24 * 3600
    DATE_0 = datetime(1970, 1, 1)
    DATE_PATTERN = '%d.%m.%Y'
    DATETIME_PATTERN = '%d.%m.%Y %H:%M:%S'
    TRADE_HOUR = timedelta(hours=16)
    SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    def __init__(self):
        self.arr = None
        self.data = None
        self.timestamp_sec = None

    def prepare(self, ticker):
        self._load(ticker)
        with db.get_db() as _db:
            start_time = time.time()
            queries = Queries(_db)
            self.data = queries.select_all_by_ticker(ticker)
            print('fetch_time', time.time() - start_time)
            self.timestamp_sec = self._get_first_timestamp(self.data[0][3])
            self.data = self._get_trade_per_batch()
            self._create_array()
            model_data = self._create_model_data()
            self._save(model_data, ticker)

    def _get_first_timestamp(self, date) -> int:
        date_from_stamp = datetime.fromtimestamp(date).strftime(self.DATE_PATTERN)
        timestamp_date = datetime.strptime(date_from_stamp, self.DATE_PATTERN) + self.TRADE_HOUR
        return (timestamp_date - self.DATE_0).total_seconds()

    def _get_trade_per_batch(self):
        return list(filter(lambda x: self._is_first_in_batch(x[3]), self.data))

    def _is_first_in_batch(self, date: int):
        if date > self.timestamp_sec:
            self.timestamp_sec += self.BATCH_TO_SEC
            return True
        return False

    def _create_array(self):
        self.arr = np.asarray([elem[4] for elem in self.data])

    def _create_model_data(self) -> dict:
        arr = self.arr
        samples_begin = max(self.SEQUENCE) + 1
        y = arr[samples_begin:]
        N = y.shape[0]
        arr = arr[::-1]
        seq = np.asarray(self.SEQUENCE)
        x = np.zeros(shape=(N, len(seq)))
        for i in range(N):
            x[i] = arr[seq]
            seq += 1
        x = np.flip(x, axis=0)
        max_val, x, y = self._normalize(x, y)
        return {'x': x, 'y': y, 'max_val': max_val}

    def _normalize(self, x, y):
        max_val = np.amax(x)
        x /= max_val
        y /= max_val
        return max_val, x, y

    def _save(self, model_data, ticker):
        with open(ticker_to_path(ticker), 'wb') as pickle_file:
            pickle.dump(model_data, pickle_file)

    def _load(self, ticker):
        with open(ticker_to_path(ticker), 'rb') as pickle_file:
            model_data = pickle.load(pickle_file)
            print(model_data)
