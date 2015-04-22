#!/usr/bin/python

from __future__ import print_function
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
        print(cursor.fetchone())
        cursor.execute("""CREATE TABLE IF NOT EXISTS Sounds(
            sound_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            filepath TEXT UNIQUE
            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Lights(
            light_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            light_address TEXT UNIQUE,
            light_color TEXT
            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
            mac_address TEXT PRIMARY KEY NOT NULL,
            username TEXT,
            sound INTEGER REFERENCES Sounds(sound_ID),
            light INTEGER REFERENCES Lights(light_ID)
            );""")
        data = cursor.fetchall()
        print(data)

main()
