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
    print("Initializing configuration...")
    init_config()
    init_loggers()

    print("Initializing database...")
    init_db()

    print("Checking the database connection...")
    with get_db() as db:
        db.execute("SELECT 1;")

    print("The database connection is working.")

    close_db()
    print("Database connection closed.")
