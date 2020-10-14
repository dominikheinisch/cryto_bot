import time
from datetime import datetime, timedelta

from database import db
from puller.queries import Queries


class Preparator:
    BATCH_TO_SEC = 24 * 3600
    DATE_0 = datetime(1970, 1, 1)
    DATE_PATTERN = '%d.%m.%Y'
    DATETIME_PATTERN = '%d.%m.%Y %H:%M:%S'
    TRADE_HOUR = timedelta(hours=16)

    def __init__(self):
        self.data = None
        self.timestamp_sec = None

    def prepare(self, ticker):
        with db.get_db() as _db:
            start_time = time.time()
            queries = Queries(_db)
            self.data = queries.select_all_by_ticker(ticker)
            print('fetch_time', time.time() - start_time)
            self.timestamp_sec = self.get_first_timestamp(self.data[0][3])
            for trade in self.get_trade_per_batch():
                print(datetime.fromtimestamp(trade[3]).strftime(self.DATETIME_PATTERN), trade)

    def get_first_timestamp(self, date) -> int:
        date_from_stamp = datetime.fromtimestamp(date).strftime(self.DATE_PATTERN)
        timestamp_date = datetime.strptime(date_from_stamp, self.DATE_PATTERN) + self.TRADE_HOUR
        return (timestamp_date - self.DATE_0).total_seconds()

    def get_trade_per_batch(self):
        return list(filter(lambda x: self.is_first_in_batch(x[3]), self.data))

    def is_first_in_batch(self, date: int):
        if date > self.timestamp_sec:
            self.timestamp_sec += self.BATCH_TO_SEC
            return True
        return False
