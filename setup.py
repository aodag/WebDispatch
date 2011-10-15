from setuptools import setup, find_packages

requires = []

try:
    import collections.OrderedDict
except ImportError:
    requires.append('ordereddict')

setup(
    name="WebDispatch",
    version="0.0",
    test_suite="webdispatch",
    license="MIT",
    install_requires=requires,
)
