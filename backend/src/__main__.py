# Entry point for the server

import sys

import uvicorn

from src.app import app
from src.cli import check_database_command, help_command


def main() -> None:
    if len(sys.argv) < 2:
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return

    if sys.argv[1] == "help":
        help_command()
        return

    if sys.argv[1] == "check-database":
        check_database_command()
        return

    print("Unknown command, use 'help' to see available commands.")


if __name__ == "__main__":
    main()
