import os
from setuptools import setup, find_packages

tests_require = [
    "pytest",
    "pytest-cov",
    "testfixtures",
    "webtest",
    "mock",
    "python-coveralls",
    "flake8",
    "pylint",
    "mypy",
]

here = os.path.dirname(__file__)
readme = None
changes = None


def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except Exception:
        return ""


readme = _read("README.rst")
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
    test_suite="webdispatch",
    license="MIT",
    install_requires=[
        "typing; python_version < '3.5'",
    ],
    tests_require=tests_require,
    extras_require={
        "testing": tests_require,
        "dev": tests_require + ["towncrier"],
    },
    url='http://github.com/aodag/WebDispatch',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points=points,
)
