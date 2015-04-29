from __future__ import print_function
import sqlite3 as sql
from dto.user import User
from lib.database.Database import Database

__author__ = 's.ehrenberg'


class SQLiteWrapper(Database):
    """ Provides a connection to the SQLite Database.
    """

    def __init__(self, db="test.db"):
        self.db = db


    def add_user(self, user):
        """
        Adds a user to the database.
        :param user: The user who will be added.
        :returns true, if adding was successful, otherwise false.
        """
        wasAddedSuccessful = False

        with sql.connect(self.db) as db_con:

            cursor = db_con.cursor()

            if not self.user_exists(cursor, user.user_mac):

                path_chunks = user.sound.split('/')
                sound_title = path_chunks[len(path_chunks) - 1]

                cursor.execute("""
                    INSERT INTO Sounds(title, filepath)
                    VALUES(?, ?);""", (sound_title, user.sound))
                cursor.execute("""SELECT sound_ID FROM Sounds WHERE rowid=?;""", cursor.lastrowid)
                sound_ID = cursor.fetchone()[0] # TODO index evtl. nicht noetig, testen!

                cursor.execute("""
                    INSERT INTO Users(name, mac_address, sound, light_color)
                    VALUES(?, ?, ?, ?);""", (
                    user.user_mac,
                    user.user_name,
                    sound_ID,
                    user.light_color))
                wasAddedSuccessful = True

            else:
                print("User already exists. Nothing inserted.")

            return wasAddedSuccessful


    def get_user(self, user_mac):
        """
        Returns the user with a given MAC address.
        :return: A user object.
        """

        user = None

        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()

            cursor.execute("SELECT * FROM Users WHERE mac_address=?", user_mac)
            mac_add, name, sound, light = cursor.fetchall()

            cursor.execute("SELECT * FROM Sounds WHERE sound_ID=?", sound)
            sound_ID, title, filepath = cursor.fetchone()

            cursor.execute("SELECT * FROM Lights WHERE light_ID=?", light)
            light_ID, light_address, light_color = cursor.fetchone()

            user = User(mac_add, name, filepath, light_ID, light_color)

        return user


    def retrieve_users(self):
        """
        Returns a list with all users.
        :return: A list containing all users.
        """
        mac_addresses = []
        users = []

        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT mac_address FROM Users")
            mac_addresses = cursor.fetchall()

        for mac_add in mac_addresses:
            user = self.get_user(mac_add)
            users.append(user)


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


    def list_sounds(self):
        """
        Provides a list of all sounds.
        :return: A list, containing the tuples (title, path).
        """
        sound_list = []
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT * FROM Sounds")
            sound_list = cursor.fetchall()

        return sound_list

