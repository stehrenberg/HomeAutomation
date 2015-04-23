from __future__ import print_function
from dto.user import User
from lib.database.Database import Database

__author__ = 's.jahreiss'

class MockDatabase(Database):
    """ Implements the database interface and serves mock data.
    """

    def __init__(self):
        """
        """
        self.users = []
        self.setup_mock()

    def retrieve_users(self):
        return self.users

    def add_user(self, user):
        self.users.append(user)
        return True

    def update_user(self, user_mac, user):
        index = self.get_index(user_mac)
        self.users[index] = user
        return True

    def delete_user(self, user_mac):
        index = self.get_index(user_mac)
        self.users.pop(index)
        return True

    def get_index(self, user_mac):
        original_user = next(user for user in self.users if user.mac == user_mac)
        return self.users.index(original_user)


    def setup_mock(self):
        markus = User('00:80:41:ae:fd:7e', 'Markus', '/sounds/beep', '1', '#ffffff')
        self.add_user(markus)
        simon = User('00:80:41:ae:fd:7d', 'Simon', '/sounds/juhu', '2', '#ffffff')
        self.add_user(simon)
        peter = User('a3', 'Peter', '/sounds/hay', '3', '#000000')
        self.add_user(peter)
