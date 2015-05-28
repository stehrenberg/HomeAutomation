from __future__ import print_function
import sqlite3 as sql
from itertools_recipes import flatten
from dto.user import User
from lib.database.Database import Database
from lib.logger.Logger import Logger

__author__ = 's.ehrenberg'


class SQLiteWrapper(Database):
    """ Provides a connection to the SQLite Database.
    """

    def __init__(self, db="test.db"):
        Database.__init__(self, db)
        self.logger = Logger()

    def add_user(self, user):
        """
        Adds a user to the database.
        :param user: The user who will be added.
        :returns true, if adding was successful, otherwise false.
        """
        was_added_successful = False
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            if not self.user_exists(cursor, user.mac):
                sound_ID = self.get_song_ID(cursor, user.sound)
                cursor.execute("""
                    INSERT INTO Users(mac_address, username, sound, light_color)
                    VALUES('%s', '%s', '%s', '%s');""" % (
                    user.mac,
                    user.name,
                    sound_ID,
                    user.light_color))
                was_added_successful = True
            else:
                self.logger.log(Logger.INFO, "User already exists. Nothing inserted.")
        return was_added_successful

    def create_sound_title(self, filepath):
        """
        Generates a sound title from a given filepath.
        :param filepath:
        :return: Filename as title
        """
        # TODO Testen, dass es auch bei Pfad 'bla.wav' funzt!
        path_chunks = filepath.split('/')
        title = path_chunks[len(path_chunks) - 1]
        self.logger.log(Logger.INFO, "title created: ", title)
        return title

    def user_exists(self, cursor, user_mac):
        """
        Checks if a given user already exists.
        :return: True, if user exists, otherwise false.
        """
        cursor.execute("""SELECT * FROM Users WHERE mac_address='%s';""" % user_mac)
        data = cursor.fetchall()
        if not data:
            return False
        else:
            return True

    def get_song_ID(self, cursor, filepath):
        """
        Retrieves the sound_ID to a sound's specified filepath.
        :return: The sound_ID or None, if sound does not exist.
        """
        cursor.execute("SELECT sound_ID from Sounds WHERE filepath='%s';" % filepath)
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return self.create_sound_ID(cursor, filepath)

    def create_sound_ID(self, cursor, filepath):
        title = self.create_sound_title(filepath)
        cursor.execute("""
            INSERT INTO Sounds(title, filepath)
            VALUES(?, ?);""", (title, filepath))
        last_row_id = cursor.lastrowid
        cursor.execute("""SELECT sound_ID FROM Sounds WHERE rowid='%s';""" % last_row_id)
        return cursor.fetchone()[0]

    def get_user(self, user_mac):
        """
        Returns the user with a given MAC address.
        :return: A user object.
        """
        user = None
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT *, rowid FROM Users WHERE mac_address='%s'" % user_mac)
            data = cursor.fetchone()
            if data:
                mac_add, name, light_color, sound, light_ID = data
                cursor.execute("SELECT * FROM Sounds WHERE sound_ID='%s'" % sound)
                sound_ID, title, filepath = cursor.fetchone()
                user = User(mac_add, name, filepath, light_ID, light_color)
            else:
                self.logger.log(Logger.INFO, "User with MAC %s could not be found." % user_mac)
        return user

    def retrieve_users(self):
        """
        Returns a list with all users.
        :return: A list containing all users.
        """
        users = []
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT mac_address FROM Users")
            mac_addresses = flatten(cursor.fetchall())
        for mac_add in mac_addresses:
            user = self.get_user(mac_add)
            users.append(user)
        return users

    def update_user(self, user_mac, user):
        """
        Updates the user with specified user_id
        """
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            sound_ID = self.get_song_ID(cursor, user.sound)
            if not sound_ID:
                sound_ID = self.create_sound_ID(cursor, user.sound)
            cursor.execute("""
                UPDATE Users
                SET light_color=?, sound=?
                WHERE mac_address=?
                ;""", (
                user.light_color,
                sound_ID,
                user_mac))
            was_update_successful = cursor.rowcount > 0
        return was_update_successful

    def delete_user(self, user_mac):
        """
        Deletes the user with the specified user_mac.
        :returns True, if user was successfully deleted, otherwise false.
        """
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("DELETE FROM Users WHERE mac_address='%s';""" % user_mac)
            deleting_successful = cursor.rowcount > 0
        return deleting_successful

    def list_sounds(self):
        """
        Provides a list of all sounds.
        :return: A list, containing the tuples (title, path).
        """
        with sql.connect(self.db) as db_con:
            cursor = db_con.cursor()
            cursor.execute("SELECT title FROM Sounds")
            sound_list = flatten(cursor.fetchall())
        return sound_list
