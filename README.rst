Trellio2
========
A high performance python3 asyncio driven framework internally uses [sanic](https://github.com/channelcat/sanic) as http server.


Installation
------------
    pip install trellio2


Getting Started
---------------

* Project structure is similar to django ::

    [projectname]/
    ├── [appdir1]/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    ├── [appdir2]/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    ├── [projectname]/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py

* Start server run following command in root directory::
    $ python manage.py runserver

* Important settings with default values.
``[projectname]/settings.py``

    - ROOT_URLCONF = "projectname.urls"
        Main entry point for project urls.
    - MAX_WORKERS = 4
        Number of server processes. Default value is equal to number of cpu cores.
    - INSTALLED_APPS = ["appdir1",
                        "appdir2",]
        List of apps

    - BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        Root directory
    - DEBUG = False
    - STRICT_SLASHES = False
    - MIDDLEWARES
        List of middlewares with path relative to root directory.
    - SERVER_HOST = "127.0.0.1"
    - SERVER_PORT = 8000
    - LOGGING = None
        config dict

* Project main urls.py
``[projectname]/urls.py``

    from trellio2.urls import url, include

    urlpatterns = [
        url('/polls', include('polls.urls'))
    ]


* App's url.py
``[appdir1]/urls.py``

    from trellio2.urls import Blueprint, url
    from .views import test_view, TestView

    urlpatterns = [
        url('/', test_view,'get'),
        url('/test/', TestView.as_view())
    ]

* You can also define urls using `Blueprint`

    from trellio2.urls import Blueprint, url
    from .views import TestView, test_view

    bp = Blueprint('polls', url_prefix='/v1/polls')
    bp.url('/', test_view, 'get')
    bp.url('/test',TestView.as_view())

    It is better to use `Blueprint` for defining urls in apps. `Blueprint` takes first argument an unique identifier which, you can provide app's name. Later it can be used for API documentation purposes.

* Defining Views
``[appdir1]/views.py``
  You can define views as functions and classes both. Views can be defined as coroutines as well.

    from trellio2.response import json_response

    async def test_view(request):
        return json_response({'test': 'success'})

  ``Class Based Views``

    from trellio2.base import View
    from trellio2.response import json_response

    class TestView(View):

        async def get(self, request): # for get http request
            return json_response({'method': 'GET'})

        async def post(self, request): # for post http request
            return json_response({'method': 'GET','data': request.json()})

    ``in urls.py``

        from trellio2.urls import Blueprint, url
        from .views import TestView

        urlpatterns = [
            url('/class-view', TestView.as_view())
        ]

* Middlewares
``[projectname]/middlewares.py``

    from trellio2.base import Middleware

    class TestMiddleware(Middleware):
        async def process_request(self, request):
            print('--------in request----')

        async def process_response(self, request, response):
            print('-------in response------', response.body)

  Including in settings
    ``[projectname]/settings.py``

        MIDDLEWARES = [
            'projectname.middlewares.TestMiddleware'
        ]
