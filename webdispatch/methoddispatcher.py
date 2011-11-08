from .base import DispatchBase
from .util import application_uri


class MethodDispatcher(DispatchBase):
    """ dispatch applications with request method.
    """
    def detect_view_name(self, environ):
        return environ['REQUEST_METHOD'].lower()

    def on_view_not_found(self, environ, start_response):
        start_response("405 Method Not Allowed",
            [('Content-type', 'text/plain')])
        return ["Method Not Allowed"]

class ActionHandlerAdapter(object):
    def __init__(self, handler_cls, action_name):
        self.handler_cls = handler_cls
        self.action_name = action_name

    def __call__(self, environ, start_response):
        handler = self.handler_cls()
        return getattr(handler, self.action_name)(environ, start_response)

class ActionDispatcher(DispatchBase):
    def __init__(self, action_var_name='action'):
        super(ActionDispatcher, self).__init__()
        self.action_var_name = action_var_name

    def register_actionhandler(self, action_handler):
        for k in action_handler.__dict__:
            if k.startswith('_'):
                continue
            app = ActionHandlerAdapter(action_handler, k)
            self.register_app(k, app)

    def detect_view_name(self, environ):
        urlvars = environ.get('wsgiorg.routing_args', [(), {}])[1]
        return urlvars.get('action')

    def on_view_not_found(self, environ, start_response):
        start_response("404 Not Found",
            [('Content-type', 'text/plain')])
        return ["Not Found %s" % application_uri(environ)]

