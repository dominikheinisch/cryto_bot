import pytest
from os import path

import settings
from database.db import get_db


@pytest.fixture
def production_db():
    if not path.isfile(settings.Database.PATH):
        pytest.skip(f'no such file: {settings.Database.PATH}')
    return get_db()
