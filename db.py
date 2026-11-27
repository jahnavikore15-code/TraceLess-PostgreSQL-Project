import os
from contextlib import contextmanager
from urllib.parse import parse_qs, urlparse
import psycopg2
from psycopg2.extras import DictCursor
from flask import g, has_app_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def get_connection():
    database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = "postgresql://" + database_url[len("postgres://"):]
        parsed = urlparse(database_url)
        query = parse_qs(parsed.query)
        connect_kwargs = {"cursor_factory": DictCursor}
        if "sslmode" not in query:
            sslmode = os.getenv("DB_SSLMODE")
            if sslmode:
                connect_kwargs["sslmode"] = sslmode
            elif parsed.hostname and parsed.hostname not in LOCAL_HOSTS:
                connect_kwargs["sslmode"] = "require"
        return psycopg2.connect(database_url, **connect_kwargs)

    if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
        raise RuntimeError(
            "DATABASE_URL environment variable is required when running on Vercel."
        )

    connect_kwargs = {
        "cursor_factory": DictCursor,
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("DB_NAME", "traceless_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
    }
    sslmode = os.getenv("DB_SSLMODE")
    if sslmode:
        connect_kwargs["sslmode"] = sslmode
    return psycopg2.connect(**connect_kwargs)


def close_db(error=None):
    if has_app_context():
        conn = g.pop("db", None)
        if conn is not None and not conn.closed:
            conn.close()


@contextmanager
def get_db():
    if has_app_context():
        conn = g.get("db")
        if conn is None or conn.closed:
            conn = get_connection()
            g.db = conn
        try:
            yield conn
            conn.commit()
        except Exception:
            if not conn.closed:
                conn.rollback()
            raise
    else:
        conn = get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            if not conn.closed:
                conn.rollback()
            raise
        finally:
            if not conn.closed:
                conn.close()


def init_db():
    schema_path = os.path.join(BASE_DIR, "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as file:
        sql = file.read()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
