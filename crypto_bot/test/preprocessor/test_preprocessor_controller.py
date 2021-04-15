import numpy as np
from decimal import Decimal
from pytest_mock import MockerFixture

from src.database.model import Trade
from src.preprocessor.preprocessor import Preprocessor
from src.preprocessor.sequencer import Sequencer


def daily_timestamp_generator():
    created_at = 1555344001
    while True:
        yield created_at
        created_at += 24 * 60 * 60


timestamp = daily_timestamp_generator()
DATA = [
    Trade(id=1, tid=0, ticker_id=0, created_at=next(timestamp), price=Decimal('5.3'), amount=Decimal('0.11888')),
    Trade(id=2, tid=1, ticker_id=0, created_at=next(timestamp), price=Decimal('10.6'), amount=Decimal('0.5')),
    Trade(id=2, tid=2, ticker_id=0, created_at=next(timestamp), price=Decimal('21.2'), amount=Decimal('0.475')),
    Trade(id=4, tid=1, ticker_id=0, created_at=next(timestamp), price=Decimal('10.6'), amount=Decimal('0.5')),
]


class TestPreprocessorController():
    def test_basic(self, mocker: MockerFixture):
        Sequencer.SEQUENCE = np.asarray([1, 2])
        mocker.patch('src.database.pg_connector.PgConnector.__init__', return_value=None)
        mocker.patch('src.database.queries.Queries.select_all_by_ticker', return_value=DATA)
        data_set = Preprocessor().prepare('whatever')._data_set
        assert np.all(data_set['prices'] == np.array([
            [Decimal('0.5'), Decimal('0.25')],
            [Decimal('1'), Decimal('0.5')],
        ]))
        assert np.all(data_set['prices_to_predict'] == np.array([Decimal('1'), Decimal('0.5')]))
        assert data_set['max_val'] == Decimal('21.2')
