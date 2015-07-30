import re
import time
from ConfigParser import SafeConfigParser

import utils


def main():    
    parser = SafeConfigParser()
    parser.read('creator.ini')
    n = parser.getint('general', 'num_accounts')
    password = parser.get('general', 'password')
    d = utils.Database()
    c = utils.ColoredOutput()
    br = utils.AnonBrowser()
    for x in range(n):
        success = False
        br.anonymize()
        while not success:
            try:
                br.method = 'GET'
                br.open('https://www.reddit.com/login')
            except Exception, e:
                c.print_error('Error connecting to reddit.com ')
                continue

            br.form = list(br.forms())[0]

            user = utils.gen_random_string(13)
            done = d.insert(user, True)
            while not done:
                user = utils.gen_random_string(13)
                done = d.insert(user, True)

            br['user'] = user
            br['passwd'] = password
            br['passwd2'] = password

            try:
                br.method = "POST"
                response = br.submit()
                response2 = br.response().read()
            except Exception, e:
                c.print_error('HTTP error, retrying')
                continue

            if "you are doing that too much" in response2:
                rateLocation = response2.find("you are doing that too much. try again in ")
                rateLimit = int(response2[rateLocation + 42 : rateLocation + 44])
                c.print_error('Rate limiting detected. Try again in {0} minutes'.format(rateLimit))
                c.print_error('Sleeping for {} minutes'.format(rateLimit))
                time.sleep(int(rateLimit))
            elif "that username is already taken" in response2:
                c.print_error('User: {0} already exists'.format(user))
            elif "username can only" in response2:
                c.print_error("User: {0} is an invalid username, can only contain numbers, letters \'-\'' and \'_\'".format(user))
            else:
                d.insert(user, False)
                success = True
                c.print_good('{} successfully created. User: {}'.format(user, x))

if __name__ == "__main__":
    main()
