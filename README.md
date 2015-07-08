# Reddit-Manipulation

So considering Reddit is already pretty crappy these days, I'm going to make it even crappier! This will be done by vote manipulation. Creating mass reddit accounts, and then using these accounts to upvote or downvote whatever I want. 

####PHASE 1: Creating mass reddit accounts
---------------------------

So the basis of this portion comes from the book *Violent Python* by TJ O'Connor. Most of what I'll be using is from a python reddit api called [PRAW](https://praw.readthedocs.org/en/v3.0.0/). But considering it doesn't really do much for account creation (and for good reason) we're going to be going through that part in Mechanize. 

The first issue I came across is using an actual proxy in order to make reddit think we are unique visitors, so as to not get rate limited. The list of proxies I had wasn't accurately hiding my ip and I actually wrote [a test script](https://github.com/THEMVFFINMAN/Reddit-Manipulation/blob/master/ProxyTester.py) to verify if it was used correctly. 

In the end, TOR seemed to be the only viable option. And even then it's sort of hacky as you have to constantly restart the TOR daemon. But it works and I made like a 1000 accounts in an hour or so. 
