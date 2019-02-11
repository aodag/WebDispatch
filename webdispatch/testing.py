""" utilities for testing
"""


def setup_environ(**kwargs):
    """ setup basic wsgi environ"""
    environ = {}
    from wsgiref.util import setup_testing_defaults

    setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


def make_env(path_info, script_name):
    """ set up basic wsgi environ"""

    from wsgiref.util import setup_testing_defaults

    environ = {"PATH_INFO": path_info, "SCRIPT_NAME": script_name}
    setup_testing_defaults(environ)
    return environ
