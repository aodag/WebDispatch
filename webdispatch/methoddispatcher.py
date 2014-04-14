""" methoddispatcher

"""

from wsgiref.util import application_uri
from .base import DispatchBase


class MethodDispatcher(DispatchBase):
    """ dispatch applications with request method.
    """
    def __init__(self, **kwargs):
        super(MethodDispatcher, self).__init__()
        for name, app in kwargs.items():
            self.register_app(name, app)

    def detect_view_name(self, environ):
        """ convert request method to view name """
        return environ['REQUEST_METHOD'].lower()

    def on_view_not_found(self, _, start_response):
        """ called when valid view is not found """

        start_response(
            "405 Method Not Allowed",
            [('Content-type', 'text/plain')])
        return [b"Method Not Allowed"]


def action_handler_adapter(handler_cls, action_name):
    """ wraps class to wsgi application dispathing action"""

    if not hasattr(handler_cls(), action_name):
        message = "{0} does'nt have attr:{1}".format(handler_cls, action_name)
        raise ValueError(message)

    def wsgiapp(environ, start_response):
        """ inner app """
        handler = handler_cls()
        return getattr(handler, action_name)(environ, start_response)
    return wsgiapp


class ActionDispatcher(DispatchBase):
    """ wsgi application dispatching actions to registered classes"""

    def __init__(self, action_var_name='action'):
        super(ActionDispatcher, self).__init__()
        self.action_var_name = action_var_name

    def register_actionhandler(self, action_handler):
        """ register class as action handler """
        for k in action_handler.__dict__:
            if k.startswith('_'):
                continue
            app = action_handler_adapter(action_handler, k)
            self.register_app(k, app)

    def detect_view_name(self, environ):
        """ get view name from routing args """
        urlvars = environ.get('wsgiorg.routing_args', [(), {}])[1]
        return urlvars.get(self.action_var_name)

    def on_view_not_found(self, environ, start_response):
        """ called when action is not found """
        start_response(
            "404 Not Found",
            [('Content-type', 'text/plain')])
        return [b"Not Found ", application_uri(environ).encode('utf-8')]
