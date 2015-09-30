"""
Provides utility functions and classes for other modules
"""
import random
import string

from colorama import deinit
from colorama import Fore
from colorama import init


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
