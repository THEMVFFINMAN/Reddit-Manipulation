# Reddit-Manipulation

This is a library for carrying out vote manipulation on Reddit.
It creates fake users for you which can be used to upvote/downvote posts and comments.
Because it interacts with the Tor daemon, and I only use Tor on Linux, this only works on Linux.

## Installation

`python setup.py install` will install the library and all of its dependencies.
See `requirements.txt` for a list of current dependencies.
This list should not change in future updates.

Also ensure that the Tor daemon is installed on your machine.

## Use

### Account creation

```
>>> import manipulator
>>> c = manipulator.Creator('/path/to/my.db', 'service tor restart', 5, 'somepassword')
>>> c.run()
```

The path to the database must be the absolute path.
The command to restart the tor daemon is system dependant.
Veryify what it is on your system.
If you have `sysvinit` on your OS then it will look like `service tor restart`.
If you have `systemd` on your OS then it will look like `systemctl restart tor.service`.
Note that in order to run these commands you will need the necessary system privileges.
This means you will have to run your command with `sudo` or as root.
After the call to `c.run()` completes you will have 5 new accounts in your database, each using the password "somepassword".

### Manipulation

*FILL ME IN*

### Ban checking

Just in case your bots start getting banned (which is unlikely), there is a class for checking all of your bots.

```
>>> import manipulator
>>> s = manipulator.Shadow('/path/to/my.db')
>>> s.run()
```

This will check all of your bots in the database.

```
>>> import manipulator
>>> s = manipulator.Shadow('/path/to/my.db')
>>> s.check_user('someusername')
```

This will check a specific username.
It returns True if the user was shadow banned and has been deleted from your database, False otherwise.

## ToDo

* Proper vote manipulation using `mechanize` (currently uses `praw`)
* Vote manipulation of comments (only can handle upvoting posts)
* Python 3 compatibility (it might be already...don't know)
