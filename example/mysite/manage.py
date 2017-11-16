#!/usr/bin/env python
import os
import sys

os.environ.setdefault("TRELLIO_SETTINGS_MODULE", "mysite.settings")

if __name__ == "__main__":
    from trellio2.app import Application

    args = sys.argv
    if len(args) > 1:
        if args[1] == 'runserver':
            app = Application('mysite')
            app.run()
