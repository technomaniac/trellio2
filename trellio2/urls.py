import types
from collections import namedtuple

Route = namedtuple('Route', 'uri handler methods')


class Include:
    def __call__(self, prefix, url_module):
        self._prefix = prefix
        self._url_module = url_module
        return self.get_urls()

    def get_urls(self):
        routes = set()
        patterns = getattr(self._url_module, 'urlpatterns', self._url_module)
        for each in patterns:
            routes.add(Route(uri=self._prefix + each.uri, handler=each.handler, methods=each.methods))
        return routes


include = Include()


def url(uri, handler, methods=None, **kwargs):
    routes = set()
    if isinstance(handler, include):
        routes.update(handler)
    elif isinstance(handler, types.FunctionType):
        if isinstance(methods, str):
            methods = [methods.upper()]
        elif isinstance(methods, list):
            methods = [m.upper() for m in methods]
        routes.add(Route(uri=uri, handler=handler, methods=methods))
    return routes
