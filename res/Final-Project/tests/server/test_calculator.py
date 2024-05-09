import sys
import unittest

sys.path.append("../..")
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from my_sqlite_database import my_sqlite_database
from src.server.calculator import Calculator


class Test_calculator(unittest.TestCase):
    # ------------------------------------ SET UPS --------------------------------------------------

    @classmethod
    def setUpClass(self):
        self.sqlite = my_sqlite_database()
        self.sqlite.connect()
        self.sqlite.cursor.execute(
            """CREATE TABLE IF NOT EXISTS USERS
        (user_id INT PRIMARY KEY, first_name VARCHAR(255),
                            last_name VARCHAR(255), birth_date DATE, mail VARCHAR(255), password VARCHAR(255),
                            gender VARCHAR(255), is_admin VARCHAR(255), allowed_to_vote VARCHAR(255))""",
        )

    @classmethod
    def tearDownClass(self):
        self.sqlite.db.commit()
        self.sqlite.cursor.execute("DROP TABLE USERS")
        self.sqlite.cursor.close()
        self.sqlite.db.close()

    def setUp(self):
        for i in range(0, 100):
            self.sqlite.cursor.execute(
                f"""INSERT INTO USERS (user_id , first_name, last_name, birth_date, mail, password, gender, is_admin,
                    allowed_to_vote) VALUES ({i}, "ofir", "ovadia", "01/01/1990", "ofir_ovadia@example.com",
                    "password123", 1, 0, 1);"""
            )

    def tearDown(self):
        self.sqlite.cursor.execute("DELETE FROM USERS")
        self.sqlite.db.commit()

    # -------------------------------------- TESTS ---------------------------------------------------

    def test_get_voter_count(self):
        self.assertEqual(Calculator.get_voter_count(self.sqlite), 0)

        self.sqlite.execute_query(
            "UPDATE USERS SET allowed_to_vote = 0 WHERE user_id < 50"
        )
        self.assertEqual(Calculator.get_voter_count(self.sqlite), 50)

        self.sqlite.execute_query(
            "UPDATE USERS SET allowed_to_vote = 0 WHERE user_id = 99"
        )
        self.assertEqual(Calculator.get_voter_count(self.sqlite), 51)

    def test_get_voter_count_by_gender(self):
        self.sqlite.execute_query("UPDATE USERS SET gender = 2 WHERE user_id < 50")
        self.assertEqual(
            Calculator.get_voter_count_by_gender(self.sqlite), [0, 0]
        )  # [male,female]

        self.sqlite.execute_query(
            "UPDATE USERS SET allowed_to_vote = 0 WHERE user_id < 50"
        )
        self.assertEqual(
            Calculator.get_voter_count_by_gender(self.sqlite), [0, 50]
        )  # [male,female]

        self.sqlite.execute_query(
            "UPDATE USERS SET allowed_to_vote = 0 WHERE user_id = 99"
        )
        self.assertEqual(
            Calculator.get_voter_count_by_gender(self.sqlite), [1, 50]
        )  # [male,female]

    def get_date_years_ago(years_ago):
        current_date = datetime.now().date()
        date_years_ago = current_date - relativedelta(years=years_ago)
        date_years_ago_str = date_years_ago.strftime("%d/%m/%Y")
        return date_years_ago_str

    def test_get_voter_count_by_age(self):
        current_time = datetime.now().date()
        # [18-25, 26-35, 36-45, 46-55, 56-65, 66+]
        eighteen_years_ago = Test_calculator.get_date_years_ago(18)

        Twentysix_years_ago = Test_calculator.get_date_years_ago(26)

        Thirtysix_years_ago = Test_calculator.get_date_years_ago(36)

        fourtysix_years_ago = Test_calculator.get_date_years_ago(46)

        fiftysix_years_ago = Test_calculator.get_date_years_ago(56)

        sixtysix_years_ago = Test_calculator.get_date_years_ago(66)

        self.sqlite.cursor.execute(
            "UPDATE USERS SET birth_date = '"
            + eighteen_years_ago
            + "' WHERE user_id BETWEEN 0 AND 9"
        )

        self.sqlite.execute_query(
            "UPDATE USERS SET birth_date = '"
            + Twentysix_years_ago
            + "' WHERE user_id BETWEEN 10 AND 24"
        )

        self.sqlite.execute_query(
            "UPDATE USERS SET birth_date = '"
            + Thirtysix_years_ago
            + "' WHERE user_id BETWEEN 25 AND 29"
        )

        self.sqlite.execute_query(
            "UPDATE USERS SET birth_date = '"
            + fourtysix_years_ago
            + "' WHERE user_id BETWEEN 30 AND 49"
        )

        self.sqlite.execute_query(
            "UPDATE USERS SET birth_date = '"
            + fiftysix_years_ago
            + "' WHERE user_id BETWEEN 50 AND 79"
        )

        self.sqlite.execute_query(
            "UPDATE USERS SET birth_date = '"
            + sixtysix_years_ago
            + "' WHERE user_id BETWEEN 80 AND 100"
        )

        self.assertEqual(
            Calculator.get_voter_count_by_age(self.sqlite), [0, 0, 0, 0, 0, 0]
        )

        self.sqlite.execute_query("UPDATE USERS SET allowed_to_vote = 0")

        self.assertEqual(
            Calculator.get_voter_count_by_age(self.sqlite),
            [10, 15, 5, 20, 30, 20],
        )


if __name__ == "__main__":
    unittest.main()
