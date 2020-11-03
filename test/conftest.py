import pytest

from database.db import get_db


@pytest.fixture
def production_db():
    return get_db()
