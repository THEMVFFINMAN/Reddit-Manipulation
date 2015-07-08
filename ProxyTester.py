# Because the cookies and user agents seemed solid the next thing to test was the proxies
# And due to this code below, I was able to determine that they didn't mask my ip address at all

import mechanize
def testProxy(url, proxy):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_proxies(proxy)
    page = browser.open(url)
    source_code = page.read()
    print source_code
    
# Cannot recommend this site enough for easily checking your ip
url = 'https://api.ipify.org?format=json'

# This is just one of the proxies I tested, but it still came back with my ip address
hideMeProxy = {'http': '183.219.152.246:8123'}
testProxy(url, hideMeProxy)
