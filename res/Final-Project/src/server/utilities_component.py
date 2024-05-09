import json
import logging
import sys

sys.path.append("..")
import time
from datetime import datetime
from threading import Thread

from algorithms import (
    calculate_totals,
    convert_structure,
    generalized_median_algorithm,
    median_algorithm,
    unite_votes,
    update_dict_ids,
)
from calculator import Calculator
from counter import Counter
from database.abstract_Database import Abstract_Database
from database.data_handler import data_handler
from database.sql_database import SQL_database
from flask import Flask, jsonify, request
from flask_cors import CORS
from node import Node
from tree import Tree
from user import User
from waitress import serve


class UtilitiesComponent:
    """This class implements the Facade software design
    This class uses all subsystems and classes and exposes to server the functions cleanly
    For loose coupling between the server and the logical side"""

    def __init__(self) -> None:
        self.database = data_handler(SQL_database(SQL_database.create_config()))

    def is_guest_user(self, id: str) -> bool:
        if User.guest_user(id):
            return True

        return False

    def check_if_user_exists(self, id: str, password: str) -> bool:
        self.database.handler.connect()
        return self.database.handler.check_if_user_exists(id, password)

    def build_current_budget(self):
        self.database.handler.connect()
        tree = self.database.handler.build_tree_from_current_budget()
        dictionary = tree.to_dict()

        # updates the 'total' values in the budget dictionary
        calculate_totals(dictionary)

        return json.dumps(dictionary, ensure_ascii=False)

    def create_user(
        self,
        id: int,
        first_name: str,
        last_name: str,
        birth_date: str,
        email: str,
        password: str,
        gender: str,
        is_admin: bool,
    ):
        converted_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        if converted_date == None:
            return None

        gender = self.gender_check(gender)
        if gender is None:
            return None

        return User(
            id, first_name, last_name, converted_date, email, password, gender, False
        )

    def gender_check(self, gender):
        if gender == "male":
            # MALE
            return 1
        elif gender == "female":
            # FEMALE
            return 2
        else:
            return None

    def is_mail_exists(self, mail: str):
        """
        >>> Return: if exsits - True
        >>> else - False
        """
        self.database.handler.connect()
        mail_exists = self.database.handler.is_mail_exists(mail)
        if mail_exists:
            return True

        return False
