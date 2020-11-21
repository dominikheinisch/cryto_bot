import numpy as np

from crypto_bot.data_preparator.sequencer import Sequencer

PRICE_0 = 0.7
PRICE_1 = 0.4
PRICE_2 = 2.0
PRICE_3 = 1.2
PRICE_4 = 0.3


class TestSequencerGenerate():
    def test_basic(self):
        SEQUENCE = [1]
        self.run_generate(sequence=SEQUENCE,
                          prices=[PRICE_0, PRICE_1, PRICE_2],
                          expected_y=[PRICE_1, PRICE_2],
                          expected_x=[[PRICE_0], [PRICE_1]])

    def test_sequence_len_2(self):
        SEQUENCE = [1, 2]
        self.run_common(sequence=SEQUENCE)

    def test_sequence_not_sorted(self):
        SEQUENCE = [2, 1]
        self.run_common(sequence=SEQUENCE)

    def test_non_continous_sequence(self):
        SEQUENCE = [1, 3]
        self.run_generate(sequence=SEQUENCE,
                          prices=[PRICE_0, PRICE_1, PRICE_2, PRICE_3, PRICE_4],
                          expected_y=[PRICE_3, PRICE_4],
                          expected_x=[[PRICE_2, PRICE_0], [PRICE_3, PRICE_1]])

    def test_sequence_without_1(self):
        SEQUENCE = [2, 3]
        self.run_generate(sequence=SEQUENCE,
                          prices=[PRICE_0, PRICE_1, PRICE_2, PRICE_3, PRICE_4],
                          expected_y=[PRICE_3, PRICE_4],
                          expected_x=[[PRICE_1, PRICE_0], [PRICE_2, PRICE_1]])

    def run_generate(self, sequence, prices, expected_y, expected_x):
        result = Sequencer(sequence=np.asarray(sequence)).generate(np.asarray(prices)).to_dict()
        assert np.all(result['y'] == np.asarray(expected_y))
        assert np.all(result['x'] == np.asarray(expected_x))

    def run_common(self, sequence):
        self.run_generate(sequence=sequence,
                          prices=[PRICE_0, PRICE_1, PRICE_2, PRICE_3],
                          expected_y=[PRICE_2, PRICE_3],
                          expected_x=[[PRICE_1, PRICE_0], [PRICE_2, PRICE_1]])


class TestSequencerNormalize():
    def test_basic(self):
        sequencer = Sequencer()
        Y = np.asarray([PRICE_2, PRICE_3])
        X = np.asarray([[PRICE_1, PRICE_0], [PRICE_2, PRICE_1]])
        sequencer._y = Y.copy()
        sequencer._x = X.copy()
        result = sequencer.normalize().to_dict()
        assert np.all(result['max_val'] == PRICE_2)
        assert np.all(result['y'] == Y / PRICE_2)
        assert np.all(result['x'] == X / PRICE_2)
