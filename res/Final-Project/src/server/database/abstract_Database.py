import sys

sys.path.append("../")
from abc import ABC, abstractmethod

from tree import Tree
from user import User


class Abstract_Database(ABC):

    """Abstruct class for handling database"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def reconnect(self):
        pass

    @abstractmethod
    def execute_query(self, query: str):
        pass

    @abstractmethod
    def create_tree_from_database(self) -> Tree:
        pass

    @abstractmethod
    def get_row_count(self, table_name: str) -> int:
        pass

    @abstractmethod
    def get_row_count_by_gender(self, table_name: str) -> list[int]:
        pass

    @abstractmethod
    def get_row_count_by_age(self, table_name: str) -> list[int]:
        pass

    @abstractmethod
    def check_if_user_exists(self, id, password) -> bool:
        pass

    @abstractmethod
    def is_mail_exists(self, mail: str) -> bool:
        pass

    @abstractmethod
    def user_id_exeisting(self, user: User) -> bool:
        pass

    @abstractmethod
    def insert_new_user(self, new_user) -> bool:
        pass

    @abstractmethod
    def build_tree_from_current_budget(self) -> Tree:
        pass

    @abstractmethod
    def store_vote(self, vote: str, user_id: int) -> bool:
        pass

    @abstractmethod
    def update_voting_option(self, user_id: str, is_allowed: bool) -> bool:
        pass

    @abstractmethod
    def check_voting_option(self, user_id: str) -> str:
        pass

    @abstractmethod
    def get_information(self) -> dict:
        pass

    @abstractmethod
    def load_user_votes(self) -> list[dict]:
        pass

    @abstractmethod
    def get_user_full_name(self, user_id: int) -> list[str]:
        pass

    @abstractmethod
    def get_user_vote(self, user_id: int):
        pass

    @abstractmethod
    def update_user_vote(self, user_id: int, vote):
        pass

    @abstractmethod
    def get_user_gender(self, user_id: int):
        pass

    @abstractmethod
    def get_user_details(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def save_new_password(self, user_id: int, new_password: str) -> bool:
        pass
