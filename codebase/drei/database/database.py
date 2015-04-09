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
        Returns a list with all users.
        :return: A list containing all users.
        """
        raise NotImplementedError()

    def update_user(self, user_id, user):
        """
        Updates the user with specified user_id
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
        self.setup_mock()

    def add_user(self, user):
        self.users.append(user)

    def retrieve_users(self):
        return self.users

    def update_user(self, user_mac, user):
        original_user = [4 if x==1 else x for x in self.users]
        original_user = user

    def delete_user(self, user_mac):
        self.users = (user for user in self.users if user.user_mac != user_mac)

    def setup_mock(self):
        markus = User('a1', 'Markus', 'beep', 'test.mp3')
        self.add_user(markus)
        simon = User('b2', 'Simon', 'juhu', 'test.mp3')
        self.add_user(simon)
        peter = User('a3', 'Peter', 'hay', 'test.mp3')
        self.add_user(peter)
