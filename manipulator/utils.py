"""
Provides utility functions and classes for other modules
"""
import cookielib
import random
import socket
import string
import subprocess
import time

import requests
from colorama import deinit
from colorama import Fore
from colorama import init
import mechanize
import socks


class ColoredOutput(object):
    """
    Class for providing colored error and normal output.
    Uses colorama and print()
    """
    def __init__(self):
        """
        Initializes colorama and sets good and error prefixes
        """
        init()
        self.good = Fore.GREEN + '[+] ' + Fore.RESET
        self.error = Fore.RED + '[-] ' + Fore.RESET

    def print_good(self, text):
        """
        Print normal output with good prefix

        :param str text: Text to be printed
        """
        print('{}{}'.format(self.good, text))

    def print_error(self, text):
        """
        Print error output with error prefix

        :param str text: Text to be printed
        """
        print('{}{}'.format(self.error, text))

    def close(self):
        """
        Deinitializes colorama
        """
        deinit()


class RedAPI(object):
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

        :param str vote: 1, -1, or 0 as a string
        :param str id: post or comment id
        :param str subreddit: the subreddit name the post is in
        """
        payload = {
            'id': id,
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

    def _change_proxy(self):
        subprocess.call(self.tor_cmd.split(), shell=False) # should check return code, but we'll just assume it works

    def anonymize(self):
        """
        Clears cookies, changes user agent, restarts Tor (for new IP)
        """
        self._change_user_agent()
        self._change_proxy()

    def _set_socket(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        #patch the socket module
        socket.socket = socks.socksocket

    def test(self):
        return requests.get('http://icanhazip.com')

class AnonBrowser(mechanize.Browser):
    """
    Class for anonymously accessing Reddit
    """
    def __init__(self, command, user_agents = []):
        """
        Initializes AnonBrowser instance

        :param str command: Command to restart tor daemon
        :param list user_agents: User agents to fake. default []
        """
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

    def anonymize(self):
        """
        Clears cookies, changes user agent, restarts Tor (for new IP)
        """
        self._clear_cookies()
        self._change_user_agent()
        self._change_proxy()

    def _set_socket(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        #patch the socket module
        socket.socket = socks.socksocket
        socket.create_connection = create_connection


def gen_random_string(len_name=10):
    """
    Generates a random string of the specified length using
    the ASCII characters excluding special chars

    :param int len_name: Specifies length of the string to generate. default 10
    :return: Random string of specified length
    :rtype: str
    """
    chars = string.ascii_letters + string.digits
    name = ''
    for i in range(len_name):
        idx = random.randint(0, len(chars)-1)
        name += chars[idx]
    return name


def create_connection(address, timeout=None, source_address=None):
    """
    Used in AnonBrowser to connect through a socks proxy

    :return: Socks socket
    """
    sock = socks.socksocket()
    sock.connect(address)
    return sock
