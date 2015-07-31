"""
Provides class for checking if a bot is shadow banned
"""
try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except:
    from urllib2 import urlopen
    from urllib2 import HTTPError


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
