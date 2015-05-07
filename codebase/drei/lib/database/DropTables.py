from __future__ import print_function
from itertools_recipes import flatten
import sqlite3 as sql
import sys, signal

def sig_int_handler(signum, stack):
    sys.exit()

def main():
    """ Use some docstring for comments!
    """

    signal.signal(signal.SIGINT, sig_int_handler)
    db_connect = None
    db = 'test.db'

    with sql.connect(db) as db_connect:
        # foreign keys are disabled by default for backwards compatibility
        db_connect.execute("""PRAGMA foreign_keys = ON;""")
        cursor = db_connect.cursor()
        cursor.execute("""PRAGMA foreign_keys;""")
        print("Deleting table Users...")
        cursor.execute("""DROP TABLE IF EXISTS Users;""")
        print("Deleting table Sounds...")
        cursor.execute("""DROP TABLE IF EXISTS Sounds;""")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Sounds' OR name='Users';")
        deleted_tables = flatten(cursor.fetchall())
        if len(deleted_tables) == 0:
            print("Tables successfully deleted.")
