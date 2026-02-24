import os
import psycopg2
import psycopg2.extras
from contextlib import contextmanager


@contextmanager
def get_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        dbname=os.getenv("DB_NAME", "mydb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def query(sql, params=None):
    with get_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def query_one(sql, params=None):
    with get_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchone()


def execute(sql, params=None):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
