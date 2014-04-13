""" utilities for testing
"""


def make_env(path_info, script_name):
    """ set up basic wsgi environ"""

    from wsgiref.util import setup_testing_defaults
    environ = {
        "PATH_INFO": path_info,
        "SCRIPT_NAME": script_name,
    }
    setup_testing_defaults(environ)
    return environ


class DummyURLGenerator(object):
    """ dummy for url generator that returns url passed initialization"""
    def __init__(self, url):
        self.url = url
        self.called = ()

    def generate(self, name, **kwargs):
        """ return url and record called """
        self.called = ('generate', name, kwargs)
        return self.url


class DummyStartResponse(object):
    """ dummy func of wsgi start_response"""
    def __init__(self):
        self.status = None
        self.headers = None

    def __call__(self, status, headers):
        self.status = status
        self.headers = headers


class DummyApp(object):
    """ dummy wsgi application """
    def __init__(self, response_body):
        self.response_body = response_body

    def __call__(self, environ, start_response):
        start_response(
            "200 OK",
            [('Content-type', 'text/plain')])
        return self.response_body
