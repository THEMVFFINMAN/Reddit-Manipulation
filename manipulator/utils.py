import cookielib
import os
import random
import socket
import sqlite3
import string
import subprocess
import time

from colorama import deinit
from colorama import Fore
from colorama import init
import mechanize
import socks


SCHEMA = 'create table usernames (id integer primary key autoincrement not null,name text not null,password text not null)'


class ColoredOutput(object):
    def __init__(self):
        init()
        self.good = Fore.GREEN + '[+] ' + Fore.RESET
        self.error = Fore.RED + '[-] ' + Fore.RESET

    def print_good(self, text):
        print('{}{}'.format(self.good, text))

    def print_error(self, text):
        print('{}{}'.format(self.error, text))

    def close(self):
        deinit()


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

    def insert(self, name, password, check):
        """
        Inserts a username into the table or checks if it exists
        :param name: a username string to be inserted
        :returns: true if inserted, false if the name is already in the db
        """
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usernames WHERE name = ?', (name,))
            data = cursor.fetchone()
            if not data:
                # it doesnt exist yet in our db
                if not check:
                    cursor.execute('INSERT INTO usernames (name, password) values (?,?)', (name,password))
                    conn.commit()
                return True
            else:
                return False

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


class AnonBrowser(mechanize.Browser):
    def __init__(self, command, user_agents = []):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.user_agents = user_agents + ['Mozilla/4.0 ',\
        'FireFox/6.01','ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = cookielib.CookieJar()
        self.set_cookiejar(self.cookie_jar)
        self._set_socket()
        self.tor_cmd = command

    def _clear_cookies(self):
        self.cookie_jar = cookielib.CookieJar()
        self.set_cookiejar(self.cookie_jar)

    def _change_user_agent(self):
        userAgent = random.choice(self.user_agents)
        self.addheaders = [('User-agent', userAgent)]

    def _change_proxy(self):
        subprocess.call(self.tor_cmd.split(), shell=False) # should check return code, but we'll just assume it works

    def anonymize(self, sleep = False):
        self._clear_cookies()
        self._change_user_agent()
        self._change_proxy()
        
        # Largely unnecessary at this point
        if sleep:
            print "Sleep Started"
            time.sleep(600)
            print "Sleeping Finished"

    def _set_socket(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        #patch the socket module
        socket.socket = socks.socksocket
        socket.create_connection = create_connection


def gen_random_string(len_name=10):
    """
    This generates a random string of the specified length using
    the ASCII characters excluding special chars
    :param len_name: optional. specifies the length of the string to return
    :returns: random string of specified length
    """
    chars = string.ascii_letters + string.digits
    name = ''
    for i in range(len_name):
        idx = random.randint(0, len(chars)-1)
        name += chars[idx]
    return name


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock
