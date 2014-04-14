""" tests for webdispatch.methoddispatcher"""
from testfixtures import compare
from webdispatch import testing


class TestMethodDispatcher(object):
    """ test for webdispatch.methoddispatcher.MethodDispatcher"""
    @staticmethod
    def _get_target():
        """ get class under test """
        from webdispatch.methoddispatcher import MethodDispatcher
        return MethodDispatcher

    def _make_one(self, *args, **kwargs):
        """ create object under test """
        return self._get_target()(*args, **kwargs)

    @staticmethod
    def _setup_environ(**kwargs):
        """ setup basic wsgi environ"""
        environ = {}
        from wsgiref.util import setup_testing_defaults
        setup_testing_defaults(environ)
        environ.update(kwargs)
        return environ

    def test_it(self):
        """ test basic using"""
        app = self._make_one(get=lambda environ, start_response: ["get"])
        environ = self._setup_environ()
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        compare(result, ["get"])

    def test_not_allowed(self):
        """ test not found views"""
        app = self._make_one(get=lambda environ, start_response: ["get"])
        environ = self._setup_environ(REQUEST_METHOD='POST')
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        compare(result, [b"Method Not Allowed"])
        compare(start_response.status, '405 Method Not Allowed')


class TestActionHandlerAdapter(object):
    """ test for webdispatch.methoddispatcher.action_handler_adapter"""
    @staticmethod
    def _call_fut(*args, **kwargs):
        """ call function under test """
        from webdispatch.methoddispatcher import action_handler_adapter
        return action_handler_adapter(*args, **kwargs)

    @staticmethod
    def _setup_environ(**kwargs):
        """ setup basic wsgi environ """
        environ = {}
        from wsgiref.util import setup_testing_defaults
        setup_testing_defaults(environ)
        environ.update(kwargs)
        return environ

    def test_call(self):
        """ test basic using """

        class DummyAction(object):
            """ dummy action class"""
            def __init__(self):
                self.message = b"Hello"

            def action(self, _, start_response):
                """ dummy action """
                start_response("200 OK",
                               [("Content-type", "text/plain")])
                return [self.message]

        target = self._call_fut(DummyAction, "action")
        environ = self._setup_environ(REQUEST_METHOD='POST')
        start_response = testing.DummyStartResponse()
        result = target(environ, start_response)
        compare(result, [b"Hello"])
        compare(start_response.status, '200 OK')


class TestActionDispatcher(object):
    """ test for webdispatch.methoddispatcher.ActionDispatcher"""
    @staticmethod
    def _get_target():
        """ get class under test"""
        from webdispatch.methoddispatcher import ActionDispatcher
        return ActionDispatcher

    def _make_one(self, *args, **kwargs):
        """ create object under test"""
        return self._get_target()(*args, **kwargs)

    @staticmethod
    def _setup_environ(**kwargs):
        """ setup wsgi environ """
        environ = {}
        from wsgiref.util import setup_testing_defaults
        setup_testing_defaults(environ)
        environ.update(kwargs)
        return environ

    def test_it(self):
        """ test for basic usage"""
        app = self._make_one()

        def test_app(environ, start_response):
            return [b'got action']

        app.register_app('test_app', test_app)
        routing_args = [(), {'action': 'test_app'}]
        environ = self._setup_environ(**{'wsgiorg.routing_args': routing_args})
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        compare(result, [b"got action"])

    def test_register_action_handler(self):
        """ test register """
        app = self._make_one()

        class DummyHandler(object):
            def test_action(self, environ, start_response):
                return [b"test action"]

        app.register_actionhandler(DummyHandler)
        routing_args = [(), {'action': 'test_action'}]
        environ = self._setup_environ(**{'wsgiorg.routing_args': routing_args})
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        compare(result, [b"test action"])

    def test_not_found(self):
        """ test called not registered action """

        app = self._make_one()
        app.register_app('test_app',
                         None)
        routing_args = [(), {'action': 'no_app'}]
        env = {'wsgiorg.routing_args': routing_args}
        environ = self._setup_environ(**env)
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        compare(start_response.status, '404 Not Found')
        compare(result,
                [b"Not Found ",
                 b"http://127.0.0.1/"])
