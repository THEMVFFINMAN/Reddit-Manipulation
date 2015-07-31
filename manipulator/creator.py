import re
import time

import utils


class Creator(object):
    def __init__(self, db_name, tor_command, num_accounts=100, password='adminssuck'):
        self.c = utils.ColoredOutput()
        self.n = num_accounts
        self.c.print_good('Will create {} accounts'.format(self.n))
        self.password = password
        self.c.print_good('Using password: {}'.format(self.password))
        self._check_tilda(db_name)
        self.db_name = db_name
        self.c.print_good('Using database: {}'.format(self.db_name))
        self.d = utils.Database(self.db_name)
        self.tor_command = tor_command
        self.c.print_good('Using tor command: {}'.format(self.tor_command))
        self.br = utils.AnonBrowser(self.tor_command)

    def _check_tilda(self, s):
        if s.startswith('~'):
            raise ValueError('Tildas not allowed. They break things.')

    def run(self):    
        for x in range(self.n):
            success = False
            self.br.anonymize()
            while not success:
                try:
                    self.br.method = 'GET'
                    self.br.open('https://www.reddit.com/login')
                except Exception, e:
                    self.c.print_error('Error connecting to reddit.com ')
                    continue

                self.br.form = list(self.br.forms())[0]

                user = utils.gen_random_string(13)
                done = self.d.insert(user, self.password, True)
                while not done:
                    user = utils.gen_random_string(13)
                    done = self.d.insert(user, self.password, True)

                self.br['user'] = user
                self.br['passwd'] = self.password
                self.br['passwd2'] = self.password

                try:
                    self.br.method = "POST"
                    response = self.br.submit()
                    response2 = self.br.response().read()
                except Exception, e:
                    self.c.print_error('HTTP error, retrying')
                    continue

                if "you are doing that too much" in response2:
                    rateLocation = response2.find("you are doing that too much. try again in ")
                    rateLimit = int(response2[rateLocation + 42 : rateLocation + 44])
                    self.c.print_error('Rate limiting detected. Try again in {0} minutes'.format(rateLimit))
                    self.br.anonymize()
                    # self.c.print_error('Sleeping for {} minutes'.format(rateLimit))
                    # time.sleep(int(rateLimit))
                elif "that username is already taken" in response2:
                    self.c.print_error('User: {0} already exists'.format(user))
                elif "username can only" in response2:
                    self.c.print_error("User: {0} is an invalid username, can only contain numbers, letters \'-\'' and \'_\'".format(user))
                else:
                    self.d.insert(user, self.password, False)
                    success = True
                    self.c.print_good('{} successfully created. User: {}'.format(user, x))
            time.sleep(2)
