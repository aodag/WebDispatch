""" test for webdispatch.paster """
from testfixtures import compare
from webdispatch import testing


class TestPaste(object):
    """ test for webdispatch.paster.make_urldispatch_application """
    @staticmethod
    def _make_env(path_info, script_name):
        """ make basic wsgi environ """
        return testing.make_env(path_info, script_name)

    @staticmethod
    def _call_fut(*args, **kwargs):
        """ call function under test """
        from webdispatch.paster import make_urldispatch_application
        return make_urldispatch_application(*args, **kwargs)

    def assert_response_body(self, app, path, expected):
        """ assert body created app on path equals expected"""
        environ = self._make_env(path, '')
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        compare(result, expected)

    def test_it(self):
        """ test basic usage """
        global_conf = {}
        patterns = """
        / = webdispatch.dummyapps:greeting
        /bye = webdispatch.dummyapps:bye"""

        application = self._call_fut(global_conf, patterns=patterns)
        self.assert_response_body(application, '/', [b'Hello'])
        self.assert_response_body(application, '/bye', [b'bye'])
