from importlib import import_module
from multiprocessing import cpu_count

from sanic.app import Sanic

from trellio2.conf import settings
from trellio2.response import Response
from trellio2.urls import url, Blueprint


class Application:
    def __init__(self, name, ssl_context=None, urlconf_name=None):
        self._name = name
        self._ssl_context = ssl_context
        self._routes = list()
        self._app = None
        self._urlconf_name = urlconf_name or settings.ROOT_URLCONF
        self._init_app()
        self._register_urls()

    def _register_urls(self):
        patterns = getattr(self.urlconf_module, 'urlpatterns', [])
        patterns.append(url('/_ping/', ping_handler, 'GET'))

        for bp in Blueprint._instances:
            self._routes.extend(bp.routes)
            self._app.blueprint(bp, url_prefix=bp.url_prefix)

        for each in patterns:
            self._routes.extend(each)
            for route in each:
                self._app.add_route(route.handler, route.uri, route.methods,
                                    strict_slashes=getattr(settings, 'STRICT_SLASHES', False))

    @property
    def urlconf_module(self):
        return import_module(self._urlconf_name)

    def run(self, **kwargs):
        host = getattr(settings, 'SERVICE_HOST', 'localhost')
        port = getattr(settings, 'SERVICE_PORT', 8000)
        workers = getattr(settings, 'MAX_WORKERS', cpu_count())
        debug = getattr(settings, 'DEBUG', False)
        log_config = getattr(settings, 'LOGGING', None)
        self._app.run(host=host, port=port, workers=workers, debug=debug, log_config=log_config, ssl=self._ssl_context,
                      **kwargs)

    def _init_app(self):
        self._app = Trellio(self._name)
        self._register_middlewares()
        try:
            from sanic_openapi import swagger_blueprint, openapi_blueprint
            self._app.blueprint(openapi_blueprint)
            self._app.blueprint(swagger_blueprint)
        except:
            pass

    def _register_middlewares(self):
        middlewares = getattr(settings, 'MIDDLEWARES', [])
        for middlware in middlewares:
            instance = self.import_class(middlware)()
            if getattr(instance, 'process_request', None):
                self._app.register_middleware(instance.process_request, attach_to='request')
            if getattr(instance, 'process_response', None):
                self._app.register_middleware(instance.process_response, attach_to='response')

    @staticmethod
    def inheritors(klass):
        subclasses = set()
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return subclasses

    @staticmethod
    def import_class(name):
        mod_path, _, cls_name = name.rpartition('.')
        mod = import_module(mod_path)
        cls = getattr(mod, cls_name)
        return cls


async def ping_handler(request):
    return Response(body='pong')


class Trellio(Sanic):
    def __init__(self, *args, **kwargs):
        super(Trellio, self).__init__(*args, **kwargs)
