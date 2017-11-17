#!/usr/bin/env python
import os
import sys

from trellio2.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("TRELLIO_SETTINGS_MODULE", "mysite.settings")

    execute_from_command_line(sys.argv)
