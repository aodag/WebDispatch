""" base dispatchers
"""
from typing import Dict, Any, Callable, Iterable, Optional


class DispatchBase(object):
    """ Base class for dispatcher application"""

    def __init__(
        self,
        applications: Dict[str, Callable] = None,
        extra_environ: Dict[str, Any] = None,
    ) -> None:

        if applications is None:
            self.applications = {}  # type: Dict[str, Callable]
        else:
            self.applications = applications
        if extra_environ is None:
            self.extra_environ = {}  # type: Dict[str, Any]
        else:
            self.extra_environ = extra_environ

    def register_app(self, name: str, app: Callable = None) -> Callable:
        """ register dispatchable wsgi application"""
        if app is None:

            def dec(app):
                """ inner decorator for register app """
                assert app is not None
                self.register_app(name, app)
                return app

            return dec
        self.applications[name] = app
        return app

    def get_extra_environ(self) -> Dict[str, Any]:
        """ returns for environ values for wsgi environ"""
        return self.extra_environ

    def detect_view_name(
        self, environ: Dict[str, Any]
    ) -> Optional[str]:  # pragma: nocover
        """ must returns view name for request """
        raise NotImplementedError()

    def on_view_not_found(
        self, environ: Dict[str, Any], start_response: Callable
    ) -> Iterable[bytes]:  # pragma: nocover
        """ called when view is not found"""
        raise NotImplementedError()

    def __call__(
        self, environ: Dict[str, Any], start_response: Callable
    ) -> Iterable[bytes]:
        extra_environ = self.get_extra_environ()
        environ.update(extra_environ)
        view_name = self.detect_view_name(environ)
        if view_name is None:
            return self.on_view_not_found(environ, start_response)

        app = self.applications.get(view_name)

        if app is None:
            return self.on_view_not_found(environ, start_response)

        return app(environ, start_response)
