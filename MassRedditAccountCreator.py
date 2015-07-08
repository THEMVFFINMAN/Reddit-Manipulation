import mechanize, cookielib, random, time, socks, socket, subprocess

# For ease of use this will create a bunch of users with the same string followed by a number and the same password
# This will come in handy further on down the road when we do vote manipulation
userName = "Some user"
passWord = "Some password"

# Necessary for it to work with mechanize
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

# Sets up TOR 
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

# This class if almost verbatim from *Violent Python*
class anonBrowser(mechanize.Browser):

    def __init__(self, user_agents = []):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.user_agents = user_agents + ['Mozilla/4.0 ',\
        'FireFox/6.01','ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = cookielib.CookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()

    def clear_cookies(self):
        self.cookie_jar = cookielib.CookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        userAgent = random.choice(self.user_agents)
        self.addheaders = [('User-agent', userAgent)]

    # This gets a new ip by resetting tor
    def change_proxy(self):
        checkTor = subprocess.check_output('service tor restart', shell = True)
        if "Stopping tor daemon...done." and "Starting tor daemon...done." in checkTor:
            print "[+] Restarted tor daemon"
        elif "Stopping tor daemon...done." and not "Starting tor daemon...done." in checkTor:
            print "[-] Error starting tor daemon"
            exit(0)
        elif not "Stopping tor daemon...done." in checkTor:
            print "[-] Error stopping tor daemon"
            exit(0)

    def anonymize(self, sleep = False):
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        
        # Largely unnecessary at this point
        if sleep:
            print "Sleep Started"
            time.sleep(600)
            print "Sleeping Finished"

def main():    
    setTOR()
    # This will create 1000 users with the same password
    for x in range(1, 1000):
        success = False

        # Ran into a socks issue that this corrects
        while not success:
    
            # First we anonymize which also sleeps for 10 minutes
            br = anonBrowser()
            
            # Next we open up reddit's login and grab the create user form
            try:
                br.open('https://www.reddit.com/login')
            except Exception, e:
                print "[-] Error connecting to reddit.com "
                continue

            br.form = list(br.forms())[0]

            # Creates a new user based on the string above and appends a number to it
            user = userName + str(x)
        
            br['user'] = user
            br['passwd'] = passWord
            br['passwd2'] = passWord

            br.method = "POST"
            response = br.submit()
            response2 = br.response().read()

            # Cleaner error handling
            if "you are doing that too much" in response2:
                rateLocation = response2.find("you are doing that too much. try again in ")
                rateLimit = int(response2[rateLocation + 42 : rateLocation + 44])
                print "[-] Rate limiting detected. Try again in {0} minutes".format(rateLimit)
            elif "that username is already taken" in response2:
                print "[-] User: {0} already exists".format(user)
            elif "username can only" in response2:
                print "[-] User: {0} is an invalid username, can only contain numbers, letters \'-\'' and \'_\'".format(user)
            else:
                print "[+] {0} successfully created.".format(user)
                success = True

if __name__ == "__main__":
    main()
