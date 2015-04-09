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
        markus = User('a1', 'Markus', 'beep', 'test.mp3')
        self.add_user(markus)
        simon = User('b2', 'Simon', 'juhu', 'test.mp3')
        self.add_user(simon)
        peter = User('a3', 'Peter', 'hay', 'test.mp3')
        self.add_user(peter)
