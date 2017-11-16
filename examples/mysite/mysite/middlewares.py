from trellio2.base import Middleware


class TestMiddleware(Middleware):
    async def process_request(self, request):
        print('--------in request----')

    async def process_response(self, request, response):
        print('-------in response------', response.body)
