import sqlite3

import settings


def get_db():
    return sqlite3.connect(
        settings.Database.PATH,
        detect_types=sqlite3.PARSE_DECLTYPES,
    )


def init_db():
    with get_db() as db:
        with open(settings.Database.SCHEMA_PATH) as f:
            db.executescript(f.read())
