import os
import sys
from importlib import import_module
from time import time

from trellio2.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "TRELLIO_SETTINGS_MODULE"


class Settings:
    def __init__(self):
        self.SETTINGS_MODULE = os.environ.get(ENVIRONMENT_VARIABLE)
        mod = import_module(self.SETTINGS_MODULE)

        tuple_settings = (
            "INSTALLED_APPS",
            "TEMPLATE_DIRS",
            "LOCALE_PATHS",
        )
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ImproperlyConfigured("The %s setting must be a list or a tuple. " % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

        if not hasattr(self, 'INSTALLED_APPS') and not self.INSTALLED_APPS:
            raise Exception('settings has no INSTALLED_APPS attribute')

        if not hasattr(self, 'BASE_DIR') and not self.BASE_DIR:
            raise Exception('settings has no BASE_DIR attribute')

        if hasattr(time, 'tzset') and self.TIME_ZONE:
            # When we can, attempt to validate the timezone. If we can't find
            # this file, no check happens and it's harmless.
            zoneinfo_root = '/usr/share/zoneinfo'
            if (os.path.exists(zoneinfo_root) and not
            os.path.exists(os.path.join(zoneinfo_root, *(self.TIME_ZONE.split('/'))))):
                raise ValueError("Incorrect timezone setting: %s" % self.TIME_ZONE)
            # Move the time zone info into os.environ. See ticket #2315 for why
            # we don't do this unconditionally (breaks Windows).
            os.environ['TZ'] = self.TIME_ZONE
            time.tzset()

        for app in self.INSTALLED_APPS:
            sys.path.append(os.path.join(self.BASE_DIR, app))

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }


settings = Settings()
