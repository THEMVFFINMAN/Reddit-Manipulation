import cmd
from ConfigParser import SafeConfigParser

from manipulator.creator import Creator
from manipulator.database import Database
from manipulator.shadow import Shadow


class BotShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.env = {}
        parser = SafeConfigParser()
        parser.read('config.ini')
        self.tor = parser.get('general', 'tor')
        self.db = parser.get('general', 'db')
        self.d = Database(self.db)
        self.c = Creator(self.db, self.tor)
        self.s = Shadow()

    def do_set_password(self, line):
        '''Specify password to make new bots with'''
        self.c.password = line

    def do_set_num_accounts(self, line):
        '''Specify num bots to make'''
        self.c.n = int(line)

    def do_create(self, line):
        '''Create new bots'''
        self.c.run()

    def do_check_user(self, line):
        '''Check if a bot is banned'''
        if self.s.check_user(line):
            print('That user is banned')
        else:
            print('That user is fine')

    def do_db_destroy(self, line):
        '''Destroy the db. Yes, really.'''
        self.d.destroy_db()

    def do_db_insert(self, line):
        '''Insert a new bot to the db'''
        u, p = line.split()
        self.d.insert(u, p)

    def do_db_get_all_names(self, line):
        '''Get all bot names in the db'''
        print(self.d.get_all_names())

    def do_exit(self, line):
        return True

    def emptyline(self):
        pass


if __name__ == '__main__':
    BotShell().cmdloop()
