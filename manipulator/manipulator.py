import random
import requests
import socket
import socks
import subprocess
import time

class Manipulator(object):
    """
    """
    def __init__(self, tor_cmd):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        ]
        self.hdrs = {
            'User-Agent': '',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.reddit.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.create_payload = {
            'api_type': 'json',
            'passwd2': '',
            'op': 'reg',
            'passwd': '',
            'dest': 'https%3A%2F%2Fwww.reddit.com%2F',
            'user': ''
        }
        self.create_url = 'https://www.reddit.com/api/register/'
        self.login_payload = {
            'op': 'login',
            'api_type': 'json',
            'user': '',
            'passwd': '',
            'dest': 'https%3A%2F%2Fwww.reddit.com%2F'
        }
        self.login_url = 'https://www.reddit.com/api/login/'
        self.vote_url = 'https://www.reddit.com/api/vote'
        self.tor_cmd = tor_cmd
        self._set_socket()
        self.anonymize()
        print "[+] Initialized Manipulator successfully"
    
    def create(self, username, password):
        """
        Creates a new reddit user
        
        :param str username: username of account to create
        :param str password: password of account to create
        """
        url = self.create_url + username
        self.create_payload['user'] = username
        self.create_payload['passwd'] = password
        self.create_payload['passwd2'] = password
        while True:
            r = requests.post(url, data=self.create_payload, headers=self.hdrs)
            if r.status_code != 200:
                continue
            if r.json()['json']['errors']:
                raise Exception(r.json()['json']['errors'])
            else:
                return

    def login(self, username, password):
        """
        Logs in to reddit and creates a requests Session to use for
        follow-up requests via this object
        
        :param str username: username to login with
        :param str password: password to login with
        """
        self.session = requests.Session()
        self.login_payload['user'] = username
        self.login_payload['passwd'] = password
        url = self.login_url + username
        while True:
            r = self.session.post(url, headers=self.hdrs, data=self.login_payload)
            if r.status_code != 200:
                continue
            if r.json()['json']['errors']:
                raise Exception(r.json()['json']['errors'])
            self.modhash = r.json()['json']['data']['modhash']
            return

    def vote(self, vote, id, subreddit):
        """
        Vote on specified comment or post.
        ID should be something like t1_cvhfg0h

        :param int vote: 1, -1, or 0 as an int (not string)
        :param str id: post or comment id
        :param str subreddit: the subreddit name the post is in
        """
        payload = {
            'id': int(id),
            'dir': vote,
            'r': subreddit,
            'uh': self.modhash
        }
        while True:
            r = self.session.post(self.vote_url, headers=self.hdrs, data=payload)
            if r.status_code != 200:
                continue
            if not r.text:
                return
            else:
                raise Exception('Voting failed. Might be the ID')

    def logout(self):
        """
        Destroy the session for the logged in user
        """
        self.modhash = ''
        self.session = None

    def _change_user_agent(self):
        self.hdrs['User-agent'] = random.choice(self.user_agents)
        print "[+] Changed User Agent Successfully"

    def _change_proxy(self):
        print "[+] Initializing Tor"
        subprocess.call(self.tor_cmd.split(), shell=False) # should check return code, but we'll just assume it works
        print "[+] Waiting 5 seconds for Tor to restart"
        time.sleep(5)
        print "[+] Changed proxy successfully"

    def anonymize(self):
        """
        Clears cookies, changes user agent, restarts Tor (for new IP)
        """
        self._change_user_agent()
        self._change_proxy()

    def _set_socket(self):
        socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
        #patch the socket module
        socket.socket = socks.socksocket
        
        print "[+] Set Socket Successfully"
        

    def test(self):
        return "[+] IP Adress: {}".format(requests.get('http://icanhazip.com').text)
