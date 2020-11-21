import numpy as np


class Sequencer:
    SEQUENCE = np.asarray([1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])

    def __init__(self, sequence=None):
        self._sequence = np.asarray(sequence if sequence is not None else self.SEQUENCE)
        self._max_val = None

    def generate(self, prices):
        self._sequence.sort()
        samples_begin = max(self._sequence)
        self._y = prices[samples_begin:]
        N = self._y.shape[0]
        prices = prices[::-1]
        seq = np.asarray(self._sequence)
        x = np.zeros(shape=(N, len(seq)))
        for i in range(N):
            x[i] = prices[seq]
            seq += 1
        self._x = np.flip(x, axis=0)
        return self

    def normalize(self):
        self._max_val = np.amax(self._x)
        self._x /= self._max_val
        self._y /= self._max_val
        return self

    def to_dict(self):
        return {'x': self._x, 'y': self._y, 'max_val': self._max_val}
