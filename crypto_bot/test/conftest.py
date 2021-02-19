import pytest
from psycopg2 import OperationalError

from src.database.pg_connector import PgConnector


@pytest.fixture
def production_db_conn():
    try:
        conn = PgConnector()
    except OperationalError as e:
        print(e)
        pytest.xfail('no connection to db')
    except KeyError as e:
        if 'PG_HOST' in e.args:
            print(e)
            pytest.xfail('no required environment variable')
    return conn
