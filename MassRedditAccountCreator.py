import mechanize, cookielib, random, time

# For ease of use this will create a bunch of users with the same string followed by a number and the same password
# This will come in handy further on down the road when we do vote manipulation
userName = "Some User Name"
passWord = "Some password"

def getProxies():
    #This is what gets a random good proxy from rmccurdy's list
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    page = browser.open('http://rmccurdy.com/scripts/proxy/good.txt')

    proxies = []

    for proxy in page.readlines():
        proxies.append({'http': proxy.replace('\n', '')})
    
    #Returns it in mechanize's format
    return proxies

# This class if almost verbatim from *Violent Python*
class anonBrowser(mechanize.Browser):

    def __init__(self, proxies = getProxies(), user_agents = []):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.proxies = proxies
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

    def change_proxy(self):
        if self.proxies:
            proxy = random.choice(self.proxies)
            self.set_proxies(proxy)

    def anonymize(self, sleep = True):
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        
        # Sometimes this is good for other reasons to implement a sleep timer
        # But for our purposes it's just to automate it arround reddit's filter
        if sleep:
            print "Sleep Started"
            time.sleep(600)
            print "Sleeping Finished"

def main():    

  # This will create 150 users with the same password
    for x in range(1, 150):
    
        # First we anonymize which also sleeps for 10 minutes
        br = anonBrowser()
        
        # Next we open up reddit's login and grab the create user form
        br.open('https://www.reddit.com/login')
        br.form = list(br.forms())[0]

        # Creates a new user based on the string above and appends a number to it
        user = userName + str(x)
    
        br['user'] = user
        br['passwd'] = passWord
        br['passwd2'] = passWord

        br.method = "POST"
        response = br.submit()
        response2 = br.response().read()
        
        # As of right now the responses aren't too helpful so once I figure out this limit rating
        # I'll come back and make something for nicer response reading
        
        if response2:
            print "{0} success".format(x)

if __name__ == "__main__":
    main()
