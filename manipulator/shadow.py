"""
Provides class for checking if a bot is shadow banned
"""
try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except:
    from urllib2 import urlopen
    from urllib2 import HTTPError
import time

import utils


class Shadow(object):
    """
    Class providing methods for checking is a user is shadow banned
    """
    def __init__(self):
        """
        Initializes instance. Adds ColoredOutput instance for printing in self.run()
        """
        self.c = utils.ColoredOutput()

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
                    self.d.delete(username)
                    return True
                elif e.code == 429:
                    continue
                else:
                    print(e)
                    continue

    def run(self, names):
        """
        Checks all names specified for shadow ban

        :param list names: List of all names to check
        """
        cnt = 0
        for name in names:
            if self.check_user(name):
                self.c.print_error('{} is shadow banned and has been removed'.format(name))
                cnt += 1
            else:
                self.c.print_good('{} is fine'.format(name))
            time.sleep(2)
        self.c.print_error('Removed {} users'.format(cnt))
