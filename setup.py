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
