"""
Provides utility functions and classes for other modules
"""
import cookielib
import random
import socket
import string
import subprocess
import time

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
