# This whole thing will probably get redone because not only have I tried
# To make PRAW use a TOR socket, I have also added the TOR proxy to the praw.ini file
# Yet even though I've test upvoted posts about 500 times, the post is unchanced

# First I'm going to try and do mechanize or requests that I know has some anonymity
# And works with TOR. If that doesn't work then I'll try to space out the upvotes more
# And if that doesn't work, we'll just see what happens when we get there

import praw
import argparse
import time
import socks
import socket
import subprocess
from random import randint

USERNAME  = "Some user"
PASSWORD  = "Some password"
USERAGENT = "Mozzarella or something"

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def setTOR():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

    #patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

    checkTor = subprocess.check_output('service tor restart', shell = True)

    if "Starting tor daemon...done." in checkTor:
        print "[+] Started tor daemon for first time"
    else:
        print "[-] Error starting tor daemon"
        exit(0)

def change_proxy():
    checkTor = subprocess.check_output('service tor restart', shell = True)
    if "Stopping tor daemon...done." and "Starting tor daemon...done." in checkTor:
        print "[+] Restarted tor daemon"
    elif "Stopping tor daemon...done." and not "Starting tor daemon...done." in checkTor:
        print "[-] Error starting tor daemon"
        exit(0)
    elif not "Stopping tor daemon...done." in checkTor:
        print "[-] Error stopping tor daemon"
        exit(0)

def randSeconds(upvotes):
    if upvotes < 50:
        return randint(5,20)
    elif upvotes < 200:
        return randint(3,10)
    else:
        return randint(1,5)

def main():
	upvotes = 0
	setTOR()

	for x in range(35, 1000):
		success = False

		while not success:

			realUserName = USERNAME + str(x)

			sleep = randint(1,3)
			print "[+] {0} sleeping for {1} seconds before upvoting".format(realUserName, sleep)
			time.sleep(sleep)

			r = praw.Reddit(USERAGENT)
			try:
				r.login(realUserName, PASSWORD, disable_warning=True)
			except Exception, e:
				print "[-] Wrong password problem, Not sure how that happened"
				success = True
				continue

			link = "https://www.reddit.com/r/lockpicking/comments/3669nb/lockpickers_of_reddit_can_you_break_this/"


			try:
				submission = r.get_submission(link)
				submission.upvote()
				print "[+] {0} upvoted the link successfully".format(realUserName)
				upvotes = upvotes + 1
				success = True
			except Exception, e:
				print e
				print "[-] Error upvoting or getting submission, retrying"
				continue

			change_proxy()

if __name__ == "__main__":
	main()