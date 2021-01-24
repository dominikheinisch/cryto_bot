import numpy as np


class Sequencer:
    SEQUENCE = np.asarray([1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])

    def __init__(self, sequence=None):
        self._sequence = np.asarray(sequence if sequence is not None else self.SEQUENCE)
        self._sequence.sort()
        self._max_val = None

    def generate(self, prices):
        max_index = np.amax(self._sequence)
        self.__generate_prices_to_predict(prices, max_index)
        self.__generate_prices(prices, max_index)
        return self

    def normalize(self):
        self._max_val = np.amax(self._prices)
        self._prices /= self._max_val
        self._prices_to_predict /= self._max_val
        return self

    def to_dict(self):
        return {'prices': self._prices, 'prices_to_predict': self._prices_to_predict, 'max_val': self._max_val}

    def __generate_prices_to_predict(self, prices, max_index):
        self._prices_to_predict = prices[max_index:]

    def __generate_prices(self, prices, max_index):
        x_size = np.size(prices) - max_index
        seq_size = np.size(self._sequence)
        sequence_row = max_index - self._sequence
        sequence_indexes = np.array([range(x_size)] * seq_size).transpose() + sequence_row
        self._prices = np.take(prices, sequence_indexes)
