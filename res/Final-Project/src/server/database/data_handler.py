import sys

sys.path.append("../..")
from server.database.abstract_Database import Abstract_Database


class data_handler:

    """This class manages what type of database we will be dealing with - shell of management"""

    def __init__(self, the_database: Abstract_Database):
        self.handler = the_database
