"""
Provides class for interacting with bot database
"""
import os
import sqlite3


SCHEMA = 'create table usernames (id integer primary key autoincrement not null,name text not null,password text not null)'


class Database(object):
    """
    Class for interacting with the bot database
    """
    def __init__(self, name):
        """
        Initializes the Database instance

        :param str name: Absolute path to the database file
        """
        self.name = name
        self._init_db()

    def delete(self, username):
        """
        Deletes a bot from the database

        :param str username: Name of the bot to delete
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usernames WHERE name = ?', (username,))
            conn.commit()
    
    def _init_db(self):
        """
        Creates a database file and initializes the table
        if it does not exist
        """
        exists = os.path.exists(self.name)
        if not exists:
            with sqlite3.connect(self.name) as conn:
                conn.executescript(SCHEMA)
                conn.commit()

    def insert(self, name, password):
        """
        Inserts a user into the table

        :param str name: Name of the bot being inserted
        :param str password: Password of the bot being inserted
        """
        if not self.check_username(name):
            with sqlite3.connect(self.name) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO usernames (name, password) values (?,?)', (name,password))
                conn.commit()

    def check_username(self, username):
        """
        Checks if bot is in database

        :param str username: Name of the bot to check
        :return: False if doesn't exist, True if exists
        :rtype: bool
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usernames WHERE name = ?', (username,))
            data = cursor.fetchone()
            if not data:
                return False
            return True

    def get_entry_by_name(self, name):
        """
        Gets database row for specified bot

        :param str name: Name of bot whose entry we want
        :return: Row or None
        :rtype: list or None
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usernames WHERE name = ?', (name,))
            data = cursor.fetchone()
            return data

    def get_entry_by_password(self, password):
        """
        Gets all rows containing <password>

        :param str password: Password in entries we want
        :return: All entries containing password
        :rtype: list
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usernames WHERE password = ?', (password,))
            rows = cursor.fetchall()
            return rows

    def get_all_names(self):
        """
        Get a list of all the usernames in the db

        :return: list containing all bot names
        :rtype: list
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM usernames')
            names = cursor.fetchall()
            return [row[0] for row in names]

    def get_all_entries(self):
        """
        Get everything

        :return: All rows
        :rtype: list
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usernames')
            rows = cursor.fetchall()
            return rows
