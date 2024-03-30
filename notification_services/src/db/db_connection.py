from contextlib import contextmanager

import psycopg2
# from constants import dsl
from psycopg2.extras import DictCursor


@contextmanager
def open_postgres_connection():
    dsn = f'postgresql+asyncpg://admin:password@localhost:5432/notify'
    dsl = {
        'dbname': 'notify',
        'user': 'admin',
        'password': 'password',
        'host': 'localhost',
        'port': '5432',
    }
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield pg_conn.cursor()
    finally:
        pg_conn.commit()
        pg_conn.close()
