
class DispatchBase(object):

    def __init__(self, **kwargs):

        self.applications = {}
        for k, v in kwargs.items():
            self.register_app(k, v)

    def register_app(self, name, app):
        self.applications[name] = app

    def __call__(self, environ, start_response):
        view_name = self.detect_view_name(environ)
        if view_name is None:
            return self.on_view_not_found(environ, start_response)

        app = self.applications.get(view_name)

        if app is None:
            return self.on_view_not_found(environ, start_response)

        return app(environ, start_response)
