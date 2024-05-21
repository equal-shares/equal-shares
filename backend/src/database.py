# This module contains the database connection pool and the database dependency for FastAPI.

import functools
from contextlib import contextmanager
from typing import Any, Callable, Generator, TypeVar

import psycopg
from psycopg.conninfo import make_conninfo
import psycopg_pool

from src.config import config
from src.exceptions import CriticalException, DBException
from src.logger import get_logger

g_pool: None | psycopg_pool.ConnectionPool = None


def _get_pool() -> psycopg_pool.ConnectionPool:
    global g_pool
    if g_pool is None:
        raise CriticalException("Database not initialized")
    return g_pool


def init_db() -> None:
    """Initialize database connection pool"""

    global g_pool
    if g_pool is not None:
        return

    try:
        g_pool = psycopg_pool.ConnectionPool(
            conninfo=make_conninfo(
                "",
                host=config.pg_host,
                port=config.pg_port,
                dbname=config.pg_database,
                user=config.pg_user,
                password=config.pg_password
            ),
            # sslmode="require",
            min_size=1,
            max_size=10,
            timeout=30,
        )
        g_pool.wait()
    except psycopg.OperationalError as e:
        get_logger().exception(e)
        raise CriticalException("Database connection failed") from e


def close_db() -> None:
    """Close database connection pool"""
    global g_pool

    if g_pool is None:
        return

    g_pool.close()
    g_pool = None


def db_dependency() -> Generator[psycopg.Connection, None, None]:
    """FastAPI dependency for database connection, used in the endpoints of the API"""

    db = _get_pool().getconn()
    try:
        yield db
    finally:
        _get_pool().putconn(db)


@contextmanager
def get_db() -> Generator[psycopg.Connection, None, None]:
    """Return database connection"""

    return db_dependency()


ReturnT = TypeVar("ReturnT")


def db_named_query(func: Callable[..., ReturnT]) -> Callable[..., ReturnT]:
    """Decorator for database named queries in the models."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> ReturnT:
        try:
            return func(*args, **kwargs)
        except psycopg.errors.DatabaseError as e:
            error_msg = str(e)
            get_logger().error(f"Database error: {error_msg}")
            get_logger().exception(e)
            raise DBException from e

    return wrapper
