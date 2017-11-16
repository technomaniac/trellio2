from distutils.core import setup

from setuptools import find_packages

setup(
    name='trellio2',
    version='0.1',
    packages=find_packages(exclude=['tests', 'examples']),
    url='https://bitbucket.org/samast/dataloader.git',
    author='Abhishek Verma',
    author_email='abhishek.verma@magicpin.in',
    description='A high performance python asyncio driven http framework',
    install_requires=['sanic', 'ujson', 'uvloop']
)
