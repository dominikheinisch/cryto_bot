from psycopg2 import connect
from os import environ


class PgConnector:
    def __init__(self):
        self.connection = connect(
            host=environ['PG_HOST'],
            user=environ['PG_USER'],
            password=environ['PG_PASSWORD'],
        )

    def executemany(self, query, vars_list=None, func=None):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.executemany(query=query, vars_list=vars_list)
                if func is not None:
                    return func(cursor)()

    def execute(self, query, vars=None, func=None):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query=query, vars=vars)
                if func is not None:
                    return func(cursor)()
