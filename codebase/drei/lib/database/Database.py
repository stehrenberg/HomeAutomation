from __future__ import print_function
import sqlite3 as sql
from dto.user import User
from codebase.drei.dto.user import User

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
        """
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            if not self.user_exists(cursor, user.user_mac):
                cursor.execute("""
                    INSERT INTO Lights(light_address, light_color)
                    VALUES(?, ?);""", (user.light_address, user.light_color))
                cursor.execute("""SELECT light_ID FROM Lights WHERE rowid=?;""", cursor.lastrowid)
                light_ID = cursor.fetchone()
                path_chunks = user.sound.split('/')
                sound_title = path_chunks[len(path_chunks)-1]
                cursor.execute("""
                    INSERT INTO Sounds(title, filepath)
                    VALUES(?, ?);""", (sound_title, user.sound))
                cursor.execute("""SELECT sound_ID FROM Sounds WHERE rowid=?;""", cursor.lastrowid)
                sound_ID = cursor.fetchone()
                cursor.execute("""
                    INSERT INTO Users(name, mac_address, sound, light)
                    VALUES(?, ?, ?, ?);""", (
                    user.user_mac,
                    user.user_name,
                    sound_ID,
                    light_ID))
            else:
                print("User already exists. Nothing inserted.")


    def get_user(self, user_mac):
        """
        Returns the user with a given MAC address.
        :return: A user object.
        """
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT * FROM Users WHERE mac_address=?", user_mac)
            mac_add, name, sound, light  = cursor.fetchall()
            cursor.execute("SELECT * FROM Sounds WHERE sound_ID=?", sound)
            sound_ID, title, filepath = cursor.fetchone()
            cursor.execute("SELECT * FROM Lights WHERE light_ID=?", light)
            light_ID, light_address, light_color  = cursor.fetchone()
            return User(mac_add, name, filepath, light_ID, light_color)


    def retrieve_users(self):
        """
        Returns a list with all users.
        :return: A list containing all users.
        """
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT mac_address, username FROM Users")
            data = cursor.fetchall()
            #create_user_list(data)


    def update_user(self, user_id, user):
        """
        Updates the user with specified user_id
        """
        raise NotImplementedError()


    def delete_user(self, user_mac):
        raise NotImplementedError()


    def user_exists(self, cursor, user_id):
        """
        Checks if a given user already exists.
        :return: True, if user exists, otherwise false.
        """
        cursor.execute("""SELECT * FROM Users WHERE mac_address='%s';""" % user_id)
        data = cursor.fetchall()
        if not data:
            return False
        else:
            return True


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
