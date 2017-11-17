import os
import sys

from trellio2.exceptions import ImproperlyConfigured


class ManagementUtility(object):
    """
    Encapsulates the logic of manage.py utilities.
    """
    name = 'runserver'

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def execute(self):
        from trellio2.app import Application
        from trellio2.conf import settings

        try:
            subcommand = self.argv[1]

            try:
                settings.INSTALLED_APPS
            except ImproperlyConfigured as exc:
                print(exc)

            if settings.configured:
                if subcommand == 'runserver':
                    app = Application(self.prog_name)
                    app.run()
                else:
                    print("invalid command, use 'python manage.py runserver' to start server")
            else:
                print("settings not configured")

        except IndexError:
            print("not enough arguments, use 'python manage.py runserver' to start server")

    def parse_args(self, args):
        new_args = {}
        for ind, arg in enumerate(args):
            if '=' in arg:
                broken = arg.split('=')
                new_args[broken[0]] = broken[1]
        return new_args


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
