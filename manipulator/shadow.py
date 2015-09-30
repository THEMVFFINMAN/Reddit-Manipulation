"""
Provides class for checking if a bot is shadow banned
"""
try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except:
    from urllib2 import urlopen
    from urllib2 import HTTPError

from .database import Database
from .utils import ColoredOutput
import os


class Shadow(object):
    """
    Class providing methods for checking is a user is shadow banned
    """
    def __init__(self):
        """
        Initializes instance.
        """
        pass

    def check_user(self, username):
        """
        Checks if username is shadowbanned or non-existant

        :param str username: Username to check
        :return: False if not banned, True if banned
        :rtype: bool
        """
        while True:
            try:
                r = urlopen('https://www.reddit.com/u/{}'.format(username)).read()
                return False
            except HTTPError as e:
                if e.code == 404:
                    return True
                elif e.code == 429:
                    continue
                else:
                    print(e)
                    continue

    def check_database(self, database):
        """
        Checks all users in database if they are shadowbanned or non-existant
        and removes them if they are

        :param str database: Database to check
        :return: none
        :rtype: void
        """
        self.c = ColoredOutput()
        self.db_name = database
        self.c.print_good('Using database: {}'.format(self.db_name))
        self.d = Database(self.db_name)

        user_count = 1
        try:
            for username in self.d.get_all_names():
                user_count = user_count + 1

                if self.check_user(username):
                    self.c.print_error("{} was shadowbanned".format(username))
                    self.d.delete(username)

                if user_count % 10 == 0:
                    self.c.print_good("{} accounts checked".format(user_count))
        except:
            self.c.print_error("Table usernames doesn't exist")

        if user_count == 1:
            self.c.print_error('{} database doesn\'t exist or is empty'.format(self.db_name))
            os.remove(self.db_name)
            return

        self.c.print_good('{} database successfully cleaned'.format(self.db_name))
        self.c.print_good('{} users in database'.format(user_count))
