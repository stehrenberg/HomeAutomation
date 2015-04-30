from __future__ import print_function

__author__ = 's.ehrenberg'
__author__ = 's.jahreiss'


class Database:
    """ Simple interface for the database.
    """
    def __init__(self, db="test.db"):
        self.db = db


    def add_user(self, user):
        """
        Adds a user to the database.
        :param user: The user who will be added.
        :return: True, if user was added, otherwise false.
        """
        raise NotImplementedError()


    def get_user(self, user_mac):
        """
        Returns the user with a given MAC address.
        :return: A user object.
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
        :return: True, if update was performed, otherwise false.
        """
        raise NotImplementedError()


    def delete_user(self, user_mac):
        """
        Deletes the user with specified user_id
        :return: True, if removal was successful, otherwise false.
        """
        raise NotImplementedError()


