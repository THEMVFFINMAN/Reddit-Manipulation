import os
import sqlite3


SCHEMA = 'create table usernames (id integer primary key autoincrement not null,name text not null,password text not null)'


class Database(object):
    def __init__(self, name):
        self.name = name
        self._init_db()

    def delete(self, username):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usernames WHERE name = ?', (username,))
            conn.commit()
    
    def _init_db(self):
        """
        Creates a database file and initializes the table(s)
        if it does not exist
        :returns: nothing
        """
        exists = os.path.exists(self.name)
        if not exists:
            with sqlite3.connect(self.name) as conn:
                conn.executescript(SCHEMA)
                conn.commit()

    def insert(self, name, password):
        """
        Inserts a user into the table

        :param name: a username string to be inserted
        """
        if not self.check_username(name):
            with sqlite3.connect(self.name) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO usernames (name, password) values (?,?)', (name,password))
                conn.commit()

    def check_username(self, username):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usernames WHERE name = ?', (username,))
            data = cursor.fetchone()
            if not data:
                return False
            return True

    def get_entry_by_name(self, name):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usernames WHERE name = ?', (name,))
            data = cursor.fetchone()
            return data

    def get_entry_by_password(self, password):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usernames WHERE password = ?', (password,))
            rows = cursor.fetchall()
            return rows

    def get_all_names(self):
        """
        Gives back a list of all the usernames in the db
        :returns: a list containing all usernames in the db
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM usernames')
            names = cursor.fetchall()
            return [row[0] for row in names]

    def get_all_entries(self):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usernames')
            rows = cursor.fetchall()
            return rows
