from utils.constants import Path


def ticker_to_path(ticker):
    return f'{Path.DATASET_DIR}{ticker}.pkl'