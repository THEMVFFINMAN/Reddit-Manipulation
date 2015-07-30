import utils


class Shadow(object):
    def __init__(self, name):
        self.d = utils.Database(name)
        self.c = utils.ColoredOutput()
        self.names = d.get_all_names()

    def run(self):
        for name in self.names:
            if utils.check_user(name):
                self.c.print_error('{} is shadow banned and has been removed'.format(name))
            else:
                self.c.print_good('{} is fine'.format(name))
