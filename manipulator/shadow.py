try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except:
    from urllib2 import urlopen
    from urllib2 import HTTPError
from ConfigParser import SafeConfigParser

import utils


class Shadow(object):
    def __init__(self, config):
        self.c = utils.ColoredOutput()
        self.parser = SafeConfigParser()
        self.parser.read(config)
        name = self.parser.get('database', 'name', vars={'name': '~/usernames.db'})
        self.c.print_good('Using database: {}'.format(name))
        self.d = utils.Database(name)
        self.names = d.get_all_names()

    def check_user(self, username):
        while True:
            try:
                r = urlopen('https://www.reddit.com/u/{}'.format(username)).read()
                return False
            except HTTPError as e:
                if e.code == 400:
                    self.d.delete(username)
                    return True
                elif e.code == 429:
                    continue
                else:
                    print(e)
                    continue

    def run(self):
        for name in self.names:
            if self.check_user(name):
                self.c.print_error('{} is shadow banned and has been removed'.format(name))
            else:
                self.c.print_good('{} is fine'.format(name))
