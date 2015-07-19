import cookielib
import random
import time
import socket
import subprocess
import string
import sqlite3
import os
import argparse

import mechanize
import socks


DB_NAME = 'usernames.db'
SCHEMA = 'create table usernames (id integer primary key autoincrement not null,name text not null)'
PASSWORD = "porpoisepie7"


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
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=100, help='The number of accounts to create')
    return parser.parse_args()


def init_db():
    """
    Creates a database file and initializes the table(s)
    if it does not exist
    :returns: nothing
    """
    exists = os.path.exists(DB_NAME)
    with sqlite3.connect(DB_NAME) as conn:
        if not exists:
            conn.executescript(SCHEMA)
            conn.commit()


def insert_to_db(name, check):
    """
    Inserts a username into the table or checks if it exists
    :param name: a username string to be inserted
    :returns: true if inserted, false if the name is already in the db
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usernames WHERE name = ?', (name,))
        data = cursor.fetchone()
        if not data:
            # it doesnt exist yet in our db
            if not check:
                cursor.execute('INSERT INTO usernames (name) values (?)', (name,))
                conn.commit()
            return True
        else:
            return False

def get_all_names():
    """
    Gives back a list of all the usernames in the db
    :returns: a list containing all usernames in the db
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM usernames')
        names = cursor.fetchall()
        return [row[0] for row in names]


# Necessary for it to work with mechanize
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

# Sets up TOR 
def setTOR():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

    #patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

    checkTor = subprocess.check_output('service tor restart', shell = True)

    if "Starting tor daemon...done." in checkTor:
        print "[+] Started tor daemon for first time"
    else:
        print "[-] Error starting tor daemon"

# This class ia almost verbatim from *Violent Python*
class anonBrowser(mechanize.Browser):

    def __init__(self, user_agents = []):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.user_agents = user_agents + ['Mozilla/4.0 ',\
        'FireFox/6.01','ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = cookielib.CookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()

    def clear_cookies(self):
        self.cookie_jar = cookielib.CookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        userAgent = random.choice(self.user_agents)
        self.addheaders = [('User-agent', userAgent)]

    # This gets a new ip by resetting tor
    def change_proxy(self):
        checkTor = subprocess.check_output('service tor restart', shell = True)
        if "Stopping tor daemon...done." and "Starting tor daemon...done." in checkTor:
            print "[+] Restarted tor daemon"
        elif "Stopping tor daemon...done." and not "Starting tor daemon...done." in checkTor:
            print "[-] Error starting tor daemon"
            exit(0)
        elif not "Stopping tor daemon...done." in checkTor:
            print "[-] Error stopping tor daemon"
            exit(0)

    def anonymize(self, sleep = False):
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        
        # Largely unnecessary at this point
        if sleep:
            print "Sleep Started"
            time.sleep(600)
            print "Sleeping Finished"

def main():    
    args = get_args()
    init_db()
    setTOR()
    for x in range(args.n):
        success = False

        # Whenever we get some error this allows us to have continuity
        while not success:
            br = anonBrowser()
            
            # We open up reddit's login and grab the create user form
            try:
                br.open('https://www.reddit.com/login')
            except Exception, e:
                print "[-] Error connecting to reddit.com "
                continue

            br.form = list(br.forms())[0]

            user = gen_random_string(13)
            done = insert_to_db(user, True)
            while not done:
                user = gen_random_string(13)
                done = insert_to_db(user, True)

            br['user'] = user
            br['passwd'] = PASSWORD
            br['passwd2'] = PASSWORD

            try:
                br.method = "POST"
                response = br.submit()
                response2 = br.response().read()
            except Exception, e:
                print "[-] Http Error, retrying"

            # Cleaner error handling
            if "you are doing that too much" in response2:
                rateLocation = response2.find("you are doing that too much. try again in ")
                rateLimit = int(response2[rateLocation + 42 : rateLocation + 44])
                print "[-] Rate limiting detected. Try again in {0} minutes".format(rateLimit)
            elif "that username is already taken" in response2:
                print "[-] User: {0} already exists".format(user)
            elif "username can only" in response2:
                print "[-] User: {0} is an invalid username, can only contain numbers, letters \'-\'' and \'_\'".format(user)
            else:
                print "[+] {0} successfully created. User: {1}".format(user, x)
                insert_to_db(user, False)
                success = True

if __name__ == "__main__":
    main()
    #for name in get_all_names():
    #    print name
