import pytest

from test.database.queries import TestQueries


@pytest.mark.slow
class TestProductionDB:
    def test_database_consistency(self, production_db_conn):
        queries = TestQueries(production_db_conn)
        for id, ticker in queries.select_all_id_ticker():
            count = queries.select_count(id)
            max_tid = queries.select_max_tid(id)
            print(f'ticker={ticker}, count={count}, max_tid={max_tid}')
            if max_tid is None:
                assert count == 0
            else:
                assert max_tid + 1 == count
