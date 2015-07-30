'''
Temporary script to migrate first db to new db schema
'''
import os

from manipulator import utils


d = utils.Database('usernames.db')
names = d.get_all_names()
os.remove('usernames.db')
d = utils.Database('usernames.db')
for name in names:
    d.insert(name, 'porpoisepie7', False)
