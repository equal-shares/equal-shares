import sys

from database.abstract_Database import Abstract_Database
from database.sql_database import *


class Calculator:
    """This static class performing all the calculations"""

    @staticmethod
    def get_voter_count(db: Abstract_Database) -> int:
        """
        How many people voted

        >>> # When nobody voted
        >>> Calculator.get_voter_count()
        0
        >>> # When 200 users voted
        >>> Calculator.get_voter_count()
        200
        """
        return db.get_row_count("USERS")

    @staticmethod
    def get_voter_count_by_gender(db: Abstract_Database) -> list[int]:  # [male,female]
        """
        Get the number of voters by gender

        >>> # When nobody voted
        >>> Calculator.get_voter_count_by_gender()
        >>> # [MALE, FEMALE]
        [0, 0]
        >>>> # When 2 males users voted
        >>> Calculator.get_voter_count_by_gender()
        [2,0]
        """
        return db.get_row_count_by_gender("USERS")

    @staticmethod
    def get_voter_count_by_age(db: Abstract_Database) -> list[int]:
        """
        Get the number of voters by age group

        >>> # When nobody voted
        >>> Calculator.get_voter_count_by_age()
        >>> # 18-25, 26-35, 36-45, 46-55, 56-65, 66+
        [0, 0, 0, 0, 0, 0]
        >>> # When 2 users voted between 18-25 age
        >>> Calculator.get_voter_count_by_age()
        [2, 0, 0, 0, 0, 0]
        """

        return db.get_row_count_by_age("USERS")
