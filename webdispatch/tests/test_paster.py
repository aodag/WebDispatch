""" test for webdispatch.paster """
import unittest
from webdispatch import testing


class PasteTests(unittest.TestCase):

    def _makeEnv(self, path_info, script_name):
        return testing.make_env(path_info, script_name)

    def _callFUT(self, *args, **kwargs):
        from webdispatch.paster import make_urldispatch_application
        return make_urldispatch_application(*args, **kwargs)

    def assertResponseBody(self, app, path, expected):
        environ = self._makeEnv(path, '')
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, expected)

    def test_it(self):
        global_conf = {}
        settings = {"patterns": """
        / = webdispatch.dummyapps:greeting
        /bye = webdispatch.dummyapps:bye"""}

        application = self._callFUT(global_conf, **settings)
        self.assertResponseBody(application, '/', [b'Hello'])
        self.assertResponseBody(application, '/bye', [b'bye'])
