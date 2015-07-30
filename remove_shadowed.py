import utils


d = utils.Database()
c = utils.ColoredOutput()
names = d.get_all_names()
for name in names:
    if utils.check_user(name):
        c.print_error('{} is shadow banned and has been removed'.format(name))
    else:
        c.print_good('{} is fine'.format(name))
