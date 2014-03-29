
class DispatchBase(object):

    def __init__(self, applications=None):

        if applications is None:
            self.applications = {}
        else:
            self.applications = applications

    def register_app(self, name, app):
        self.applications[name] = app

    def get_extra_environ(self):
        return {}

    def __call__(self, environ, start_response):
        environ.update(self.get_extra_environ())
        view_name = self.detect_view_name(environ)
        if view_name is None:
            return self.on_view_not_found(environ, start_response)

        app = self.applications.get(view_name)

        if app is None:
            return self.on_view_not_found(environ, start_response)

        return app(environ, start_response)
