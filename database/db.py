import sqlite3


def get_db():
    return sqlite3.connect(
        'database/db.sqlite',
        detect_types=sqlite3.PARSE_DECLTYPES,
    )


def init_db():
    with get_db() as db:
        with open('database/schema.sql') as f:
            db.executescript(f.read())
