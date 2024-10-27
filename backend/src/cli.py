# CLI for maintains

import json
import os.path
import sys

from src.algorithm.public import PublicEqualSharesInput, public_equal_shares
from src.config import init_config
from src.database import close_db, get_db, init_db
from src.logger import init_loggers


def help_command() -> None:
    print("Available commands:")
    print("python -m src                                                      - Start the server")
    print("python -m src help                                                 - Show this message")
    print("python -m src check-database                                       - Check the database connection")
    print("python -m src run-algorithm [input-json-path]                      - Run the algorithm")
    print("python -m src run-algorithm [input-json-path] [results-json-path]  - Run the algorithm")


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


def run_algorithm_command() -> None:
    if len(sys.argv) < 2:
        print("Error: input-json-path is required.")
        return

    input_json_path = sys.argv[2]
    results_json_path = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(input_json_path):
        print(f"Error: input-json-path '{input_json_path}' does not exist.")
        return

    if results_json_path is not None and os.path.exists(results_json_path):
        print(f"Error: results-json-path '{results_json_path}' already exists.")
        return

    with open(input_json_path, "r") as f:
        data = json.load(f)

    res = public_equal_shares(PublicEqualSharesInput(**data))

    if results_json_path:
        with open(results_json_path, "w") as f:
            json.dump(res.model_dump(), f, indent=2)
