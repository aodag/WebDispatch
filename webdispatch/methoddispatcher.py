
class MethodDispatcher(object):
    """ dispatch applications with request method.
    """

    def __init__(self, **kwargs):

        self.applications = kwargs.copy()

    def __call__(self, environ, start_response):
        app = self.applications.get(environ['REQUEST_METHOD'].lower())

        if app is None:
            return self.not_allowed(environ, start_response)

        return app(environ, start_response)

    def not_allowed(self, environ, start_response):
        start_response("405 Method Not Allowed",
            [('Content-type', 'text/plain')])
        return ["Method Not Allowed"]
