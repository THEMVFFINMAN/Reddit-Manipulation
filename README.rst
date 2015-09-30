.. image:: https://www.redditstatic.com/about/assets/reddit-logo.png

This is a library for carrying out vote manipulation on Reddit.
It creates fake users for you which can be used to upvote/downvote posts and comments.
Because it interacts with the Tor daemon, and I only use Tor on Linux, this only works on Linux.

Installation
------------

``python setup.py install`` will install the library and all of its dependencies.
See ``requirements.txt`` for a list of current dependencies.
This list should not change in future updates.

Also ensure that the Tor daemon is installed on your machine.

Use
---

Account creation
~~~~~~~~~~~~~~~~

::

    >>> from manipulator import Manipulator
    >>> m = Manipulator('service tor restart')
    >>> m.create('someusername', 'somepassword')

The command to restart the tor daemon is system dependant.
Veryify what it is on your system.
If you have ``sysvinit`` on your OS then it will look like ``service tor restart``.
If you have ``systemd`` on your OS then it will look like ``systemctl restart tor.service``.
Note that in order to run these commands you will need the necessary system privileges.
This means you will have to run your command with ``sudo`` or as root.
If there is an issue with the account creation, an exception will be raised.
It is best to wrap the call in a try/except clause.

Manipulation
~~~~~~~~~~~~

Assuming you have created a ``Manipulator`` object, vote manipulation is simple.
This class exposes a ``vote()`` function that takes in a value of 1, -1, or 0
along with a post or comment ID and the subreddit name.
If I were downvoting a post in ``/r/learnpython`` I would do ``m.vote(-1, 't3_id', 'learnpython')``.
For a post, prepend ``t3_`` to the ID from the URL, and ``t1_`` for a comment.

Ban checking
~~~~~~~~~~~~

Just in case your bots start getting banned (which is unlikely), there is a class for checking all of your bots.

::

    >>> from manipulator import Shadow
    >>> s = Shadow()
    >>> s.check_user('someusername')

This will check a specific username.
It returns True if the user was shadow banned, False otherwise.
Put this in a loop to check all the desired users and delete them if they are banned.

Database management
~~~~~~~~~~~~~~~~~~~

In case you want to play with your database of bots, the ``Database`` class is provided.
You can use whatever data store you like, but this class is provided for ease of use.

::

    >>> from manipulator import Database
    >>> d = Database('/path/to/my.db')

You can now insert new users, delete users by name, get all entries, get a single entry, get all entries with a certain password,
or drop everything. If the need exists, you can also check if a user is in the db.

Docs
----

To generate the docs, you first must install ``sphinx``.
From the root directory of this project, run ``sphinx-apidoc -f -o docs/ manipulator/``.
Then change into the ``docs`` directory and run ``make html``.
The freshly built docs will be in ``docs/_build/html``.

You can see a live version of the docs at http://thaweatherman.pythonanywhere.com.
Actually, no you can't because it isn't there any more.

ToDo
----

* Python 3 compatibility (it might be already...don't know)
