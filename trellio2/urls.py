import types
from collections import namedtuple
from importlib import import_module

from sanic.blueprints import Blueprint as BP

from trellio2.conf import settings

Route = namedtuple('Route', 'uri handler methods')


class Blueprint(BP):
    _instances = []

    def __init__(self, *args, **kwargs):
        super(Blueprint, self).__init__(*args, **kwargs)
        self._instances.append(self)

    def url(self, uri, handler, methods=None, **kwargs):

        strict_slashes = getattr(settings, 'STRICT_SLASHES', False)

        if isinstance(handler, list):
            for _ in handler:
                for each in _:
                    self.add_route(handler=each.handler, uri=each.uri, methods=each.methods,
                                   strict_slashes=strict_slashes)

        elif isinstance(handler, types.FunctionType):
            if isinstance(methods, str):
                methods = [methods.upper()]
            elif isinstance(methods, list):
                methods = [m.upper() for m in methods]
            self.add_route(handler=handler, uri=uri, methods=methods, strict_slashes=strict_slashes)


def url(uri, handler, methods=None, **kwargs):
    routes = []
    if isinstance(handler, list):
        for _ in handler:
            for each in _:
                routes.append(Route(uri=uri + each.uri, handler=each.handler, methods=each.methods))

    elif isinstance(handler, types.FunctionType):
        if isinstance(methods, str):
            methods = [methods.upper()]
        elif isinstance(methods, list):
            methods = [m.upper() for m in methods]
        routes.append(Route(uri=uri, handler=handler, methods=methods))
    return routes


class Include:
    def __call__(self, url_module):
        mod = import_module(url_module)
        return getattr(mod, 'urlpatterns', [])


include = Include()
