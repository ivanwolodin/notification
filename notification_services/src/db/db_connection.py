from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

from core.config import config


@contextmanager
def open_postgres_connection():
    dsl = {
        'dbname': config.PG_DB,
        'user': config.PG_USER,
        'password': config.PG_PASSWORD,
        'host': config.PG_HOST,
        'port': config.PG_PORT,
    }
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield pg_conn.cursor()
    finally:
        pg_conn.commit()
        pg_conn.close()
