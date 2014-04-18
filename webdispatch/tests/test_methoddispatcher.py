""" tests for webdispatch.methoddispatcher"""
import mock
from testfixtures import compare, ShouldRaise
from webdispatch.testing import setup_environ


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

    def test_it(self):
        """ test basic using"""
        app = self._make_one(get=lambda environ, start_response: ["get"])
        environ = setup_environ()
        start_response = mock.Mock()
        result = app(environ, start_response)
        compare(result, ["get"])

    def test_not_allowed(self):
        """ test not found views"""
        app = self._make_one(get=lambda environ, start_response: ["get"])
        environ = setup_environ(REQUEST_METHOD='POST')
        start_response = mock.Mock()
        result = app(environ, start_response)
        compare(result, [b"Method Not Allowed"])
        start_response.assert_called_with(
            '405 Method Not Allowed', [('Content-type', 'text/plain')])


class TestActionHandlerAdapter(object):
    """ test for webdispatch.methoddispatcher.action_handler_adapter"""
    @staticmethod
    def _call_fut(*args, **kwargs):
        """ call function under test """
        from webdispatch.methoddispatcher import action_handler_adapter
        return action_handler_adapter(*args, **kwargs)

    def test_call(self):
        """ test basic using """

        class DummyAction(object):
            """ dummy action class"""
            def __init__(self):
                self.message = b"Hello"

            def get_message(self):
                """ get message to return body"""
                return self.message

            def action(self, _, start_response):
                """ dummy action """
                start_response("200 OK",
                               [("Content-type", "text/plain")])
                return [self.get_message()]

        target = self._call_fut(DummyAction, "action")
        environ = setup_environ(REQUEST_METHOD='POST')
        start_response = mock.Mock()
        result = target(environ, start_response)
        compare(result, [b"Hello"])
        start_response.assert_called_with(
            '200 OK', [('Content-type', 'text/plain')])

    def test_invalid_name(self):
        """ test using invalid attr name """

        with ShouldRaise(ValueError):
            self._call_fut(object, "actionx")


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

    def test_it(self):
        """ test for basic usage"""
        app = self._make_one()

        def test_app(*_):
            """ dummy app"""
            return [b'got action']

        app.register_app('test_app', test_app)
        routing_args = [(), {'action': 'test_app'}]
        environ = setup_environ()
        environ.update({'wsgiorg.routing_args': routing_args})
        start_response = mock.Mock()
        result = app(environ, start_response)
        compare(result, [b"got action"])

    def test_register_action_handler(self):
        """ test register """
        app = self._make_one()

        class DummyHandler(object):
            """ dummy handler """

            @staticmethod
            def get_body():
                """ get body to return action """
                return [b"test action"]

            def test_action(self, *_):
                """ dummy action """
                return self.get_body()

        app.register_actionhandler(DummyHandler)
        routing_args = [(), {'action': 'test_action'}]
        environ = setup_environ()
        environ.update({'wsgiorg.routing_args': routing_args})
        start_response = mock.Mock()
        result = app(environ, start_response)
        compare(result, [b"test action"])

    def test_not_found(self):
        """ test called not registered action """

        app = self._make_one()
        app.register_app('test_app',
                         None)
        routing_args = [(), {'action': 'no_app'}]
        env = {'wsgiorg.routing_args': routing_args}
        environ = setup_environ()
        environ.update(env)
        start_response = mock.Mock()
        result = app(environ, start_response)
        start_response.assert_called_with(
            '404 Not Found', [('Content-type', 'text/plain')])

        compare(result,
                [b"Not Found ",
                 b"http://127.0.0.1/"])
