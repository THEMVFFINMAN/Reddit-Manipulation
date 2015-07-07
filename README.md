# Reddit-Manipulation

So considering Reddit is already pretty crappy these days, I'm going to make it even crappier!

####PHASE 1: Creating mass reddit accounts
---------------------------

So the basis of this portion comes from the book *Violent Python* by TJ O'Connor. Most of what I'll be using is from a python reddit api called [PRAW](https://praw.readthedocs.org/en/v3.0.0/). But considering it doesn't really do much for account creation (and for good reason) we're going to be going through that part in Mechanize. 

After fixing some small errors the big problem I'm working through right now is getting reddit to allow rapid account creation without it realizing that it is the same "user". For example, after it creates a new account it changes user agent, removes the cookie, and changes proxy, yet reddit still recognizes it. Until then it's just set to create an account every 10 minutes because that's what the limit is. 
