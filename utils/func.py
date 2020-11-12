from os import path
from time import time

import settings


def named_timer(log_name=''):
    def timer(func):
        def wrapper(*args, **kwargs):
            start_time = time()
            res = func(*args, **kwargs)
            print(f'{log_name} took {(time() - start_time):.2f}sec')
            return res
        return wrapper
    return timer


def ticker_to_path(ticker: str) -> str:
    return path.join(settings.Datasets.DIR, f'{ticker}.pkl')
