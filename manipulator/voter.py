"""
Provides classes and methods for voting with bots
"""
import utils

class Voter(object):
    """
    A class which provides methods for up/down voting posts and comments
    by a specified user
    """
    def __init__(self, tor_command):
        self.c = utils.ColoredOutput()
        self.br = utils.AnonBrowser(tor_command)

    def upvote_post(self, username, password):
