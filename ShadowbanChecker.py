'''
So Reddit admins are trying to fingerprint me now. So now when I match their fingerprint which is usually an ip address along 
with the browser type or something like that, they shadowban me. This emails me to know when it gets shadowbanned. 

Admins are doing some funky things where they're not shadowbanning me just not allowing me access to accounts I create
under my fingerprint so I might have to change this a little bit. 
'''
import praw
import smtplib
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
WAIT = 60
userName = "redditUsername"
email = "yourgmailaddress"
emailPassword = "yourgmailpassword"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.ehlo()
server.login(email, emailPassword)

r = praw.Reddit("Admins amirite")
user = r.get_redditor(userName)

creationTime = user.created_utc
message = MIMEMultipart()
message['From'] = email
message['To'] = email
message['Subject'] = userName
body = "{0} compromised after {1} time running".format(user,time.strftime("%H:%M:%S", time.localtime(time.time() - creationTime)))
message.attach(MIMEText(body, 'plain'))
text = message.as_string()

while True:
    try:
        user = r.get_redditor(userName)
        print "[+] Sleeping {0} seconds".format(WAIT)
        time.sleep(WAIT)
        
    except Exception, e:
        server.sendmail(email, email, text)
        
