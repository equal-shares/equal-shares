import sys

sys.path.append("../..")
import sqlite3
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from src.server.database.abstract_Database import Abstract_Database
from src.server.tree import Tree
from src.server.user import User


class my_sqlite_database(Abstract_Database):
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = sqlite3.connect("tests.db")
        self.cursor = self.db.cursor()

    def disconnect(self):
        self.cursor.close()
        self.db.close()

    def reconnect(self):
        self.cursor.close()
        self.db.close()
        self.db = sqlite3.connect("tests.db")
        self.cursor = self.db.cursor()

    def execute_query(self, query: str):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.db.commit()

            return results

        except:
            print(f'The query: "{query} " \n faild  ')

    def get_row_count(self, table_name: str) -> int:
        query = f"SELECT COUNT(*) FROM {table_name} WHERE allowed_to_vote=0"
        result = self.execute_query(query)
        return result[0][0]

    def get_row_count_by_gender(self, table_name: str) -> list[int]:
        male_query = (
            f"SELECT COUNT(*) FROM {table_name} WHERE gender=1 AND allowed_to_vote=0"
        )

        female_query = (
            f"SELECT COUNT(*) FROM {table_name} WHERE gender=2 AND allowed_to_vote=0"
        )

        try:
            self.cursor.execute(male_query)
            male_result = self.cursor.fetchone()

            self.cursor.execute(female_query)
            female_result = self.cursor.fetchone()

        except sqlite3.Error as err:
            print(f"An error occurred while executing the query: {err}")

        return [male_result[0], female_result[0]]

    def get_row_count_by_age(self, table_name: str) -> list[int]:
        # get the dates
        eighteen_years_ago = my_sqlite_database.get_date_years_ago(18)
        twentyfive_years_ago = my_sqlite_database.get_date_years_ago(25)
        twentysix_years_ago = my_sqlite_database.get_date_years_ago(26)
        thirtyfive_years_ago = my_sqlite_database.get_date_years_ago(35)
        thirtysix_years_ago = my_sqlite_database.get_date_years_ago(36)
        fourtyfive_years_ago = my_sqlite_database.get_date_years_ago(45)
        fourtysix_years_ago = my_sqlite_database.get_date_years_ago(46)
        fiftyfive_years_ago = my_sqlite_database.get_date_years_ago(55)
        fiftysix_years_ago = my_sqlite_database.get_date_years_ago(56)
        sixtyfive_years_ago = my_sqlite_database.get_date_years_ago(65)
        sixtysix_years_ago = my_sqlite_database.get_date_years_ago(66)

        # get the number of users by group age

        # 18-25
        eighteen_twentyfive_years_ago_query = f"""SELECT COUNT(*) FROM {table_name} WHERE
                                    birth_date BETWEEN '{twentyfive_years_ago}' AND '{eighteen_years_ago}'
                                    AND allowed_to_vote = '0' """
        eighteen_twentyfive_years_ago_result = self.execute_query(
            eighteen_twentyfive_years_ago_query
        )

        # 26-35
        twentysix_thirtyfive_years_ago_query = f"""SELECT COUNT(*) FROM {table_name} WHERE
                                    birth_date BETWEEN '{thirtyfive_years_ago}' AND '{twentysix_years_ago}'
                                    AND allowed_to_vote = '0' """
        twentysix_thirtyfive_years_ago_result = self.execute_query(
            twentysix_thirtyfive_years_ago_query
        )

        # 36-45
        thirtysix_fourtyfive_years_ago_query = f"""SELECT COUNT(*) FROM {table_name} WHERE
                                    birth_date BETWEEN '{fourtyfive_years_ago}' AND '{thirtysix_years_ago}'
                                    AND allowed_to_vote = '0' """
        thirtysix_fourtyfive_years_ago_result = self.execute_query(
            thirtysix_fourtyfive_years_ago_query
        )

        # 46-55
        fourtysix_fiftyfive_years_ago_query = f"""SELECT COUNT(*) FROM {table_name} WHERE
                                    birth_date BETWEEN '{fiftyfive_years_ago}' AND '{fourtysix_years_ago}'
                                    AND allowed_to_vote = '0' """
        fourtysix_fiftyfive_years_ago_result = self.execute_query(
            fourtysix_fiftyfive_years_ago_query
        )

        # 55-65
        fiftysix_sixtyfive_years_ago_query = f"""SELECT COUNT(*) FROM {table_name} WHERE
                                    birth_date BETWEEN '{sixtyfive_years_ago}' AND '{fiftysix_years_ago}'
                                    AND allowed_to_vote = '0' """
        fiftysix_sixtyfive_years_ago_result = self.execute_query(
            fiftysix_sixtyfive_years_ago_query
        )

        # 60+
        sixtysix_years_ago_query = f"""SELECT COUNT(*) FROM {table_name} WHERE
                                    birth_date<='{sixtysix_years_ago}'
                                    AND allowed_to_vote = '0' """
        sixtysix_years_ago_result = self.execute_query(sixtysix_years_ago_query)

        return [
            eighteen_twentyfive_years_ago_result[0][0],
            twentysix_thirtyfive_years_ago_result[0][0],
            thirtysix_fourtyfive_years_ago_result[0][0],
            fourtysix_fiftyfive_years_ago_result[0][0],
            fiftysix_sixtyfive_years_ago_result[0][0],
            sixtysix_years_ago_result[0][0],
        ]

    @staticmethod
    def _get_date_years_ago(years_ago):
        """
        Calculates the date that was 'years_ago' years ago from the current date and returns it as a string in the
        format 'yyyy-mm-dd'.

        Args:
            years_ago (int): The number of years ago to calculate the date for.

        Returns:
            str: The date that was 'years_ago' years ago from the current date, in the format 'yyyy-mm-dd'.
        """
        current_date = datetime.now().date()
        date_years_ago = current_date - timedelta(days=365 * years_ago)
        date_years_ago_str = date_years_ago.strftime("%d/%m/%Y")
        return date_years_ago_str

    @staticmethod
    def get_date_years_ago(years_ago):
        current_date = datetime.now().date()
        date_years_ago = current_date - relativedelta(years=years_ago)
        date_years_ago_str = date_years_ago.strftime("%d/%m/%Y")
        return date_years_ago_str

    # ------------------------------- Redundant methods ----------------------------------------------

    def create_tree_from_database(self) -> Tree:
        pass

    def check_if_user_exists(self, id, password) -> bool:
        pass

    def user_mail_exeisting(self, user: User) -> bool:
        pass

    def user_id_exeisting(self, user: User) -> bool:
        pass

    def insert_new_user(self, new_user) -> bool:
        pass

    def build_tree_from_current_budget(self) -> Tree:
        pass

    def store_vote(self, vote: str, user_id: int) -> bool:
        pass

    def update_voting_option(self, user_id: str, is_allowed: bool) -> bool:
        pass

    def check_voting_option(self, user_id: str) -> bool:
        pass

    def get_information(self) -> dict:
        pass

    def load_user_votes(self) -> list[dict]:
        pass

    def get_user_full_name(self, user_id: int) -> list[str]:
        pass

    def get_user_vote(self, user_id: int):
        pass

    def update_user_vote(self, user_id: int, vote):
        pass

    def get_user_gender(self, user_id: int):
        pass

    def get_user_details(self, user_id: int) -> dict:
        pass

    def save_new_password(self, user_id: int, new_password: str) -> bool:
        pass

    def is_mail_exists(self, mail: str) -> bool:
        pass