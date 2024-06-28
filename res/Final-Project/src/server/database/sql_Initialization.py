import os
import sys

sys.path.append("../")

import logging

import mysql.connector
import pandas
from dotenv import find_dotenv, load_dotenv

from node import Node
from tree import Tree

LOGֹ_FORMAT = "%(levelname)s, time: %(asctime)s , line: %(lineno)d- %(message)s "
# Create and configure logger
logging.basicConfig(filename="database_logging.log", level=logging.DEBUG, filemode="w")
logger = logging.getLogger()


# -*- coding: utf-8 -*-


class SQLInitializer:

    """A class that initializes the database"""

    # Static var
    database_name = "db_budget_system"

    @staticmethod
    def initialize_database_connection():
        dotenv_file = find_dotenv(".env")
        load_dotenv(dotenv_file)

        db = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("ADMIN_USER"),
            password=os.environ.get("ADMIN_PASSWORD"),
        )
        return db

    @staticmethod
    def establish_database_connection():
        db = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("ADMIN_USER"),
            password=os.environ.get("ADMIN_PASSWORD"),
            database="db_budget_system",
        )
        cursor = db.cursor()
        return db, cursor

    @staticmethod
    def create_database(cursor, database_name: str) -> None:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(
                database_name
            )
        )  # db_budget_system

    @staticmethod
    def create_table(mycursor, table_name: str, table_columns: str) -> None:
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_columns})")

    @staticmethod
    def delete_table(mycursor, table_name: str) -> None:
        mycursor.execute(f"DROP TABLE IF EXISTS {table_name} ")

    @staticmethod
    def clean_database(cursor) -> None:
        # Clean database
        SQLInitializer.delete_table(cursor, "CURRENT_BUDGET")
        SQLInitializer.delete_table(cursor, "USERS_VOTES")
        SQLInitializer.delete_table(cursor, "USERS")
        SQLInitializer.delete_table(cursor, "INFORMATION")

    @staticmethod
    def insert_to_current_budget_table(mycursor, node: Node) -> None:
        mycursor.execute(
            """INSERT INTO CURRENT_BUDGET (node_id, name, description, parent_id, budget_amount)
                       VALUES (%s, %s, %s, %s, %s)""",
            (
                node.get_id(),
                node.get_name(),
                node.get_description(),
                node.get_parent_id(),
                node.get_allocated_budget_amount(),
            ),
        )
        for child in node.get_children():
            SQLInitializer.insert_to_current_budget_table(mycursor, child)

    @staticmethod
    def load_and_insert_to_current_budget_table(cursor, db) -> None:
        path = "../../../dataset/"
        df = pandas.read_csv(path + "national_budget.csv", encoding="utf-8")
        # remove double quotes from relevant columns
        cols_to_clean = [
            "שם רמה 1",
            "שם רמה 2",
            "שם סעיף",
            "שם תחום",
            "שם תכנית",
            "שם תקנה",
        ]
        df[cols_to_clean] = df[cols_to_clean].apply(lambda x: x.str.replace('"', ""))
        num_rows = len(df)
        for i in range(1, num_rows):
            row = df.iloc[i, :]
            cursor.execute(
                """INSERT INTO CURRENT_BUDGET (kod_one, name_one,
                            kod_two, name_two, kod_three, name_three, kod_four, name_four, kod_five, name_five,
                            kod_six, name_six, takziv)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    int(row[0]),
                    row[1],
                    int(row[2]),
                    row[3],
                    int(row[4]),
                    row[5],
                    int(row[6]),
                    row[7],
                    int(row[8]),
                    row[9],
                    int(row[10]),
                    row[11],
                    str(row[12]) + "000",
                ),
            )
        db.commit()

    @staticmethod
    def load_information_to_information_table(cursor, db) -> None:
        path = "../../../dataset/"
        df = pandas.read_csv(path + "information.csv", encoding="utf-8")
        num_rows = len(df)
        for i in range(0, num_rows):
            row = df.iloc[i, :]
            cursor.execute(
                """INSERT INTO INFORMATION (name, details)
                        VALUES (%s, %s)""",
                (row[0], row[1]),
            )

        db.commit()

    @staticmethod
    def build_tree_from_csv() -> Tree:
        path = "../../dataset/"
        df = pandas.read_csv(path + "national_budget.csv", encoding="utf-8")

        root = Node(
            id=0, name="root", description="I am root", parent=None, budget_amount=0
        )
        tree = Tree(root)
        num_rows = len(df)
        for i in range(1, num_rows):
            row = df.iloc[i, :]
            row_list = row.tolist()
            node_id = int(row_list[0])
            node_name = row_list[1]
            if not tree.node_exists(int(node_id), node_name):
                node = Node(id=int(node_id), name=node_name, parent=0)
                tree.add_node_by_id_and_name(0, "root", node)

        for i in range(1, num_rows):
            row = df.iloc[i, :]
            row_list = row.tolist()
            node_id = int(row_list[2])
            node_name = row_list[3]
            if not tree.node_exists(int(node_id), node_name):
                node = Node(id=int(node_id), name=node_name, parent=int(row_list[0]))
                parent_id = int(row_list[0])
                parent_name = row_list[1]
                tree.add_node_by_id_and_name(parent_id, parent_name, node)

        for i in range(1, num_rows):
            row = df.iloc[i, :]
            row_list = row.tolist()
            node_id = int(row_list[4])
            node_name = row_list[5]
            if not tree.node_exists(int(node_id), node_name):
                node = Node(id=int(node_id), name=node_name, parent=int(row_list[2]))
                parent_id = int(row_list[2])
                parent_name = row_list[3]
                tree.add_node_by_id_and_name(parent_id, parent_name, node)

        for i in range(1, num_rows):
            row = df.iloc[i, :]
            row_list = row.tolist()
            node_id = int(row_list[6])
            node_name = row_list[7]
            if not tree.node_exists(int(node_id), node_name):
                node = Node(id=int(node_id), name=node_name, parent=int(row_list[4]))
                parent_id = int(row_list[4])
                parent_name = row_list[5]
                tree.add_node_by_id_and_name(parent_id, parent_name, node)

        for i in range(1, num_rows):
            row = df.iloc[i, :]
            row_list = row.tolist()
            node_id = int(row_list[8])
            node_name = row_list[9]
            if not tree.node_exists(int(node_id), node_name):
                node = Node(id=int(node_id), name=node_name, parent=int(row_list[6]))
                parent_id = int(row_list[6])
                parent_name = row_list[7]
                tree.add_node_by_id_and_name(parent_id, parent_name, node)

        for i in range(1, num_rows):
            row = df.iloc[i, :]
            row_list = row.tolist()
            node_id = int(row_list[10])
            node_name = row_list[11]
            if not tree.node_exists(int(node_id), node_name):
                node = Node(
                    id=int(node_id),
                    name=node_name,
                    parent=int(row_list[8]),
                    budget_amount=float(row_list[12]),
                )
                parent_id = int(row_list[8])
                parent_name = row_list[9]
                tree.add_node_by_id_and_name(parent_id, parent_name, node)

        return tree

    def Load_datasets(cursor, db):
        SQLInitializer.load_information_to_information_table(cursor, db)
        SQLInitializer.load_and_insert_to_current_budget_table(cursor, db)

    def build_DB(cursor, db):
        # Build database
        SQLInitializer.create_table(
            cursor,
            "CURRENT_BUDGET",
            """kod_one INT, name_one VARCHAR(1000),
                                kod_two INT, name_two VARCHAR(1000), kod_three INT, name_three VARCHAR(1000),
                                kod_four INT, name_four VARCHAR(1000), kod_five INT, name_five VARCHAR(1000),
                                kod_six INT, name_six VARCHAR(1000), takziv VARCHAR(255)""",
        )
        SQLInitializer.create_table(
            cursor,
            "USERS",
            """user_id INT PRIMARY KEY, first_name VARCHAR(255),
                                last_name VARCHAR(255), birth_date DATE, mail VARCHAR(255), password VARCHAR(255),
                                gender VARCHAR(255), is_admin VARCHAR(255), allowed_to_vote VARCHAR(255)""",
        )
        SQLInitializer.create_table(
            cursor, "USERS_VOTES", "user_id VARCHAR(255), vote TEXT(4294967295)"
        )
        SQLInitializer.create_table(
            cursor, "INFORMATION", "name VARCHAR(50), details VARCHAR(1000)"
        )

        # Load datasets
        SQLInitializer.Load_datasets(cursor, db)

    @staticmethod
    def setup_database_environment():
        """Establishes a connection to the server, creates the database, and disconnects."""
        try:
            db = SQLInitializer.initialize_database_connection()
            cursor = db.cursor()
            SQLInitializer.create_database(cursor, SQLInitializer.database_name)
        except Exception as e:
            logger.error(f"Error setting up database environment: {e}")
            raise
        finally:
            try:
                db.disconnect()
            except Exception as e:
                logger.error(f"Error closing database connection: {e}")
                raise


if __name__ == "__main__":
    # Connect server
    SQLInitializer.setup_database_environment()

    db, cursor = SQLInitializer.establish_database_connection()

    # Clean database
    SQLInitializer.clean_database(cursor)

    # create & build database
    SQLInitializer.build_DB(cursor, db)
