import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
STRICT_SLASHES = True

INSTALLED_APPS = [
    'polls'
]

MIDDLEWARES = [
    'mysite.middlewares.TestMiddleware'
]

ROOT_URLCONF = 'mysite.urls'
