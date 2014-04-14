""" base dispatchers
"""


class DispatchBase(object):
    """ Base class for dispatcher application"""

    def __init__(self, applications=None):

        if applications is None:
            self.applications = {}
        else:
            self.applications = applications

    def register_app(self, name, app):
        """ register dispatchable wsgi application"""
        self.applications[name] = app

    def get_extra_environ(self):
        """ returns for environ values for wsgi environ"""
        return {}

    def detect_view_name(self, environ):  # pragma: nocover
        """ must returns view name for request """
        raise NotImplementedError()

    def on_view_not_found(self, environ, start_response):  # pragma: nocover
        """ called when view is not found"""
        raise NotImplementedError()

    def __call__(self, environ, start_response):
        extra_environ = self.get_extra_environ()
        environ.update(extra_environ)
        view_name = self.detect_view_name(environ)
        if view_name is None:
            return self.on_view_not_found(environ, start_response)

        app = self.applications.get(view_name)

        if app is None:
            return self.on_view_not_found(environ, start_response)

        return app(environ, start_response)
