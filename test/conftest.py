import pytest
from os import path

import crypto_bot.settings as settings
from crypto_bot.database.db import get_db


@pytest.fixture
def production_db():
    if not path.isfile(settings.Database.PATH):
        pytest.skip(f'no such file: {settings.Database.PATH}')
    return get_db()
