# Reddit-Manipulation

This is a library for carrying out vote manipulation on Reddit.
It creates fake users for you which can be used to upvote/downvote posts and comments.

## Installation

`python setup.py install` will install the library and all of its dependencies.
See `requirements.txt` for a list of current dependencies.
This list should not change in future updates.

## Use

### Account creation

```
>>> import manipulator
>>> c = manipulator.Creator('/path/to/config.ini')
>>> c.run()
```
This will use the values specified in `config.ini` to get the number of accounts to create and the password to use for each account.
The `config.ini` also needs to have an absolute path to a database file specified.
After the call to `c.run()` completes you will have `n` new accounts in your database.

### Manipulation

*FILL ME IN*

### Ban checking

Just in case your bots start getting banned (which is unlikely), there is a class for checking all of your bots.

```
>>> import manipulator
>>> s = manipulator.Shadow('/path/to/config.ini')
>>> s.run()
```

This will check all of your bots in the database.
Currently, checking one user is not supported.

## ToDo

* Proper vote manipulation using `mechanize` (currently uses `praw`)
* Vote manipulation of comments (only can handle upvoting posts)
