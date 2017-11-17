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

* Important settings

    - ROOT_URLCONF : Main entry point for project urls, value for above example 'projectname.urls'
    - MAX_WORKERS : Number of server processes. Default value is equal to number of cpu cores.
    - INSTALLED_APPS : List of apps. Value for above example
                       ["appdir1",
                        "appdir2",]
    - BASE_DIR : Root directory, default value
                 os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    - DEBUG : Default value is False
    - STRICT_SLASHES : Default value is False
    - MIDDLEWARES : List of middlewares with path.