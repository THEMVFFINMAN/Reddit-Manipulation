# The issue was the proxies, so now I'm running it through Tor
# But the secret to getting Tor to give you a new ip address whenever you want
# Is to just manually start and stop TOR

import socks, mechanize, socket, subprocess, time

# Necessary for it to work with mechanize
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

# This is just setting it up to check if tor is running and if not
# to try and run it, and if that also gives an error, it just exits
def setTOR():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

    #patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

    try:
        #Checks to see if tor is running
        subprocess.check_call('pgrep tor', shell = False)
    except Exception, e:
        try:
            #Checks to see if you can restart tor
            checkTor = subprocess.check_output('service tor restart', shell = True)

            if "Starting tor daemon...done." in checkTor:
                print "[+] Started tor daemon for first time"
            else:
                print "[-] Error starting tor daemon"
        except Exception, e:
            # This is for when you just can't run tor for whatever reason
            print "[-] Error - Cannot start tor"
            exit(0)

# This is our test to see what our ip address is
def testProxy(url):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    page = browser.open(url)
    source_code = page.read()
    print "[+] IP Address: {0}".format(source_code[7:len(source_code) - 2])

def main():
    # I cannot recommend this site enough for easily checking your ip address through code
    url = 'https://api.ipify.org?format=json'

    # This graps Tor's process id and prints it out
    torPID = subprocess.check_output('pgrep tor', shell = True)
    pid = torPID.split('\n')[0]
    print "[+] TOR PID: {0}".format(pid)
    
    # Now we actually test and see what our ip address is
    testProxy(url)
    
    # Finally we restart Tor with some error protection
    checkTor = subprocess.check_output('service tor restart', shell = True)
    if "Stopping tor daemon...done." and "Starting tor daemon...done." in checkTor:
        print "[+] Restarted tor daemon"
    elif "Stopping tor daemon...done." and not "Starting tor daemon...done." in checkTor:
        print "[-] Error starting tor daemon"
        exit(0)
    elif not "Stopping tor daemon...done." in checkTor:
        print "[-] Error stopping tor daemon"
        exit(0)

if __name__ == "__main__":
    setTOR()
    # Runs 5 times to really be sure. I guess
    for x in range (0, 5):
        main()
