# Reddit-Manipulation

So considering Reddit is already pretty crappy these days, I'm going to make it even crappier! This will be done by vote manipulation. Creating mass reddit accounts, and then using these accounts to upvote or downvote whatever I want. 

####PHASE 1: Creating mass reddit accounts
---------------------------

So the basis of this portion comes from the book *Violent Python* by TJ O'Connor. Most of what I'll be using is from a python reddit api called [PRAW](https://praw.readthedocs.org/en/v3.0.0/). But considering it doesn't really do much for account creation (and for good reason) we're going to be going through that part in Mechanize. 

The first issue I came across is using an actual proxy in order to make reddit think we are unique visitors, so as to not get rate limited. The list of proxies I had wasn't accurately hiding my ip and I actually wrote [a test script](https://github.com/THEMVFFINMAN/Reddit-Manipulation/blob/master/ProxyTester.py) to verify if it was used correctly. 

In the end, TOR seemed to be the only viable option. And even then it's sort of hacky as you have to constantly restart the TOR daemon. But it works and I made like a 1000 accounts in an hour or so. 

####PHASE 2: Post manipulation
---------------------------

Eventually reddit will switch to OAUTH and most of this won't work and won't nearly be this easy. Anyways, the idea is that you'll be able to pass in a reddit link with either upvote or downvote and the accounts will do it. They'll be spaced out by a random number of seconds so as to seem random. 

It has run into some interesting issues. But unfortunately I think I maybe have been sloppy as my main reddit account was shadowbanned: ![alt text](http://i.imgur.com/md7nJXa.png "RIP /u/blendt")

So until I can figure out how they figured it out, this project is going on hiatus. It just means I'll have to go through many more shadowbanned accounts until I figure this out. 

UPDATE!! So far as long as I space them out about 10 seconds to 20 seconds apart, I can still do upvote/downvote manipulation. So far I've done it successfully for 500 upvotes and it went undetected for 7 days. This was on a subreddit that didn't allow any other posters so it was controlled. Will update after further tests.
