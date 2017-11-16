from asyncio.coroutines import iscoroutine, coroutine

from sanic.views import HTTPMethodView


class View(HTTPMethodView):
    pass


class Middleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(Middleware, self).__init__()

    def __call__(self, request):
        if getattr(self, 'process_request', None):
            if not iscoroutine(self.process_request):
                self.process_request = coroutine(self.process_request)

        if getattr(self, 'process_response', None):
            if not iscoroutine(self.process_response):
                self.process_response = coroutine(self.process_response)
