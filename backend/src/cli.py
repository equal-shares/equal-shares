# CLI for maintains

from src.config import init_config
from src.logger import init_loggers
from src.database import init_db, get_db, close_db


def help_command() -> None:
    print("Available commands:")
    print("python -m src                - Start the server")
    print("python -m src help           - Show this message")
    print("python -m src check-database - Check the database connection")


def check_database_command() -> None:
    print("Version 1")

    print("Initializing configuration...")
    init_config()
    init_loggers()

    from src.config import config
    import psycopg_pool
    from psycopg.conninfo import make_conninfo

    print("Initializing database...")
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
        max_size=2,
        timeout=30,
    )
    print(make_conninfo(
            "",
            host=config.pg_host,
            port=config.pg_port,
            dbname=config.pg_database,
            user=config.pg_user,
            password=config.pg_password
    ))
    print("Database connection pool initialized")
    try:
        g_pool.wait()
    except Exception as e:
        print(e)
        print("Database connection failed")
        raise e
    print("Database connection pool ready")

    g_pool.close()

    # print("Checking the database connection...")
    # with get_db() as db:
    #   db.execute("SELECT 1;")

    # print("The database connection is working.")

    # close_db()
    # print("Database connection closed.")
