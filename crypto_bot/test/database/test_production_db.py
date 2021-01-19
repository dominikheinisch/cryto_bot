import pytest

from test.database.queries import TestQueries


@pytest.mark.slow
class TestProductionDB:
    def test_database_consistency(self, production_db):
        for id, ticker in TestQueries().select_all_id_ticker(production_db):
            count = TestQueries().select_count(production_db, id)
            max_tid = TestQueries().select_max_tid(production_db, id)
            print(f'ticker={ticker}, count={count}, max_tid={max_tid}')
            assert max_tid + 1 == count
