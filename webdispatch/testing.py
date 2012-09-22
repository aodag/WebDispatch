def make_env(path_info, script_name):

    from wsgiref.util import setup_testing_defaults
    environ = {
        "PATH_INFO": path_info,
        "SCRIPT_NAME": script_name,
    }
    setup_testing_defaults(environ)
    return environ

class DummyURLGenerator(object):
    def __init__(self, url):
        self.url = url

    def generate(self, name, **kwargs):
        self.called = ('generate', name, kwargs)
        return self.url

class DummyStartResponse(object):
    def __call__(self, status, headers):
        self.status = status
        self.headers = headers

class DummyApp(object):
    def __init__(self, response_body):
        self.response_body = response_body

    def __call__(self, environ, start_response):
        start_response("200 OK",
            [('Content-type', 'text/plain')])
        return self.response_body

greeting = DummyApp([b'Hello'])
bye = DummyApp([b'bye'])
