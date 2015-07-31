try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except:
    from urllib2 import urlopen
    from urllib2 import HTTPError
import os
import time
from ConfigParser import SafeConfigParser

import utils


class Shadow(object):
    def __init__(self, config):
        name = os.path.expanduser('~/usernames.db')
        defaults = {
            'db_name': name
        }
        self.c = utils.ColoredOutput()
        self._check_tilda(config)
        self.parser = SafeConfigParser(defaults=defaults)
        self.parser.read(config)
        name = self.parser.get('database', 'db_name')
        self._check_tilda(name)
        self.c.print_good('Using database: {}'.format(name))
        self.d = utils.Database(name)
        self.names = self.d.get_all_names()

    def _check_tilda(self, s):
        if s.startswith('~'):
            raise ValueError('Tildas not allowed. They break things.')

    def check_user(self, username):
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

    def run(self):
        cnt = 0
        for name in self.names:
            if self.check_user(name):
                self.c.print_error('{} is shadow banned and has been removed'.format(name))
                cnt += 1
            else:
                self.c.print_good('{} is fine'.format(name))
            time.sleep(2)
        self.c.print_error('Removed {} users'.format(cnt))
