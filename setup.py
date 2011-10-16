from setuptools import setup, find_packages

requires = []
import os

try:
    import collections.OrderedDict
except ImportError:
    requires.append('ordereddict')

here = os.path.dirname(__file__)
readme = None
changes = None

def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except:
        return None

readme = _read("README.txt")
changes = _read("CHANGES.txt")

setup(
    name="WebDispatch",
    author="Atsushi Odagiri",
    author_email="aodagx@gmail.com",
    description="dispatch request on wsgi application.",
    long_description=readme + "\n" + changes,
    version="0.0",
    test_suite="webdispatch",
    license="MIT",
    install_requires=requires,
    url='http://github.com/aodag/WebDispatch',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
    ],
)
