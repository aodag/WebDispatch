from setuptools import setup, find_packages

requires = []
import os

try:
    from collections import OrderedDict
except ImportError:
    requires.append('ordereddict')

here = os.path.dirname(__file__)
readme = None
changes = None

def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except:
        return ""

readme = _read("README.txt")
changes = _read("CHANGES.txt")

points = {
    "paste.app_factory": [
        "url=webdispatch.paster:make_urldispatch_application",
    ],
}

setup(
    name="WebDispatch",
    author="Atsushi Odagiri",
    author_email="aodagx@gmail.com",
    description="dispatch request on wsgi application.",
    long_description=readme + "\n" + changes,
    version="1.0b5",
    test_suite="webdispatch",
    license="MIT",
    install_requires=requires,
    url='http://github.com/aodag/WebDispatch',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
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
    entry_points=points,
)
