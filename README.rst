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

    - ROOT_URLCONF = 'projectname.urls'
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
    - LOGGING
        config dict
