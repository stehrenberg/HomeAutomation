from dto.user import User

__author__ = 's.jahreiss'


class Database:
    """ Simple interface for the database.
    """
    def add_user(self, user):
        """
        Adds a user to the database.
        :param user: The user who will be added.
        """
        raise NotImplementedError()

    def retrieve_users(self):
        """

        :return: A list containing all users.
        """
        raise NotImplementedError()


class MockDatabase(Database):
    """ Implements the database interface and serves mock data.
    """
    def __init__(self):
        """
        """
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def retrieve_users(self):
        return self.users

    def setup_mock(self):
        markus = User(1, 'Markus', 'beep', 'a1')
        self.add_user(markus)
        simon = User(2, 'Simon', 'juhu', 'b2')
        self.add_user(simon)
        peter = User(3, 'Peter', 'hay hay', 'a3')
        self.add_user(peter)
