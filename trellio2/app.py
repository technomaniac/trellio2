from importlib import import_module
from multiprocessing import cpu_count

from pip.utils import cached_property
from sanic import Sanic

from .conf import settings


class Application:
    def __init__(self, name, ssl_context=None, urlconf_name=None):
        self._name = name
        self._ssl_context = ssl_context
        self._routes = set()
        self._app = Sanic(self._name)
        self._urlconf_name = urlconf_name or settings.ROOT_URLCONF
        self._resolve_urls()

    def _resolve_urls(self):
        if not hasattr(settings, 'INSTALLED_APPS') and not settings.INSTALLED_APPS:
            raise Exception('settings has no INSTALLED_APPS attribute')

        if not hasattr(settings, 'BASE_DIR') and not settings.BASE_DIR:
            raise Exception('settings has no BASE_DIR attribute')

        patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)

        for each in patterns:
            self._routes.update(each)
            for route in each:
                self._app.add_route(route.handler, route.uri, route.methods,
                                    strict_slashes=getattr(settings, 'STRICT_SLASHES', False))

    @cached_property
    def urlconf_module(self):
        if isinstance(self._urlconf_name, str):
            return import_module(self._urlconf_name)
        else:
            return self._urlconf_name

    def run(self):
        host = getattr(settings, 'SERVICE_HOST', 'localhost')
        port = getattr(settings, 'SERVICE_PORT', 8000)
        workers = getattr(settings, 'MAX_WORKERS', cpu_count())
        debug = getattr(settings, 'DEBUG', False)
        log_config = getattr(settings, 'LOGGING', None)
        self._app.run(host=host, port=port, workers=workers, debug=debug, log_config=log_config, ssl=self._ssl_context)
