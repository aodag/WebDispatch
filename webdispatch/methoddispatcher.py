from .util import application_uri

class DispatchBase(object):

    def __init__(self, **kwargs):

        self.applications = {}
        for k, v in kwargs.items():
            self.register_app(k, v)

    def register_app(self, name, app):
        self.applications[name] = app

    def __call__(self, environ, start_response):
        view_name = self.detect_view_name(environ)
        app = self.applications.get(view_name)

        if app is None:
            return self.on_view_not_found(environ, start_response)

        return app(environ, start_response)

class MethodDispatcher(DispatchBase):
    """ dispatch applications with request method.
    """
    def detect_view_name(self, environ):
        return environ['REQUEST_METHOD'].lower()

    def on_view_not_found(self, environ, start_response):
        start_response("405 Method Not Allowed",
            [('Content-type', 'text/plain')])
        return ["Method Not Allowed"]

class ActionDispatcher(DispatchBase):
    def __init__(self, action_var_name='action'):
        super(ActionDispatcher, self).__init__(self)
        self.action_var_name = action_var_name

    def detect_view_name(self, environ):
        urlvars = environ.get('wsgiorg.routing_args', [(), {}])[1]
        return urlvars.get('action')

    def on_view_not_found(self, environ, start_response):
        start_response("404 Not Found",
            [('Content-type', 'text/plain')])
        return ["Not Found %s" % application_uri(environ)]

