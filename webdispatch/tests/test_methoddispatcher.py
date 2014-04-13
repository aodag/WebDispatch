""" tests for webdispatch.methoddispatcher"""
import unittest
from webdispatch import testing


class MethodDispatcherTests(unittest.TestCase):
    def _getTarget(self):
        from webdispatch.methoddispatcher import MethodDispatcher
        return MethodDispatcher

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def _setup_environ(self, **kwargs):
        environ = {}
        from wsgiref.util import setup_testing_defaults
        setup_testing_defaults(environ)
        environ.update(kwargs)
        return environ

    def test_it(self):
        app = self._makeOne(get=lambda environ, start_response: ["get"])
        environ = self._setup_environ()
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, ["get"])

    def test_not_allowed(self):
        app = self._makeOne(get=lambda environ, start_response: ["get"])
        environ = self._setup_environ(REQUEST_METHOD='POST')
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, [b"Method Not Allowed"])
        self.assertEqual(start_response.status, '405 Method Not Allowed')


class ActionHandlerAdapterTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from webdispatch.methoddispatcher import action_handler_adapter
        return action_handler_adapter(*args, **kwargs)

    def _setup_environ(self, **kwargs):
        environ = {}
        from wsgiref.util import setup_testing_defaults
        setup_testing_defaults(environ)
        environ.update(kwargs)
        return environ

    def test_call(self):
        class DummyAction(object):
            def action(self, environ, start_response):
                start_response("200 OK",
                               [("Content-type", "text/plain")])
                return [b"Hello"]

        target = self._callFUT(DummyAction, "action")
        environ = self._setup_environ(REQUEST_METHOD='POST')
        start_response = testing.DummyStartResponse()
        result = target(environ, start_response)
        self.assertEqual(result, [b"Hello"])
        self.assertEqual(start_response.status, '200 OK')


class ActionDispatcherTests(unittest.TestCase):
    def _getTarget(self):
        from webdispatch.methoddispatcher import ActionDispatcher
        return ActionDispatcher

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def _setup_environ(self, **kwargs):
        environ = {}
        from wsgiref.util import setup_testing_defaults
        setup_testing_defaults(environ)
        environ.update(kwargs)
        return environ

    def test_it(self):
        app = self._makeOne()

        def test_app(environ, start_response):
            return [b'got action']

        app.register_app('test_app', test_app)
        routing_args = [(), {'action': 'test_app'}]
        environ = self._setup_environ(**{'wsgiorg.routing_args': routing_args})
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, [b"got action"])

    def test_register_action_handler(self):
        app = self._makeOne()

        class DummyHandler(object):
            def test_action(self, environ, start_response):
                return [b"test action"]

        app.register_actionhandler(DummyHandler)
        routing_args = [(), {'action': 'test_action'}]
        environ = self._setup_environ(**{'wsgiorg.routing_args': routing_args})
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, [b"test action"])

    def test_not_found(self):
        app = self._makeOne()
        app.register_app('test_app',
                         None)
        routing_args = [(), {'action': 'no_app'}]
        env = {'wsgiorg.routing_args': routing_args}
        environ = self._setup_environ(**env)
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(start_response.status, '404 Not Found')
        self.assertEqual(result,
                         [b"Not Found ",
                          b"http://127.0.0.1/"])
