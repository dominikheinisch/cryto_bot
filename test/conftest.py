import pytest
# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ..database.db import get_db


@pytest.fixture
def production_db():
    return get_db()
