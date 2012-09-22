import unittest
from . import testing

class URLMapperTests(unittest.TestCase):
    def _getTarget(self):
        from .urldispatcher import URLMapper
        return URLMapper

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_empty(self):
        target = self._makeOne()

        result = target.lookup("")

        self.assertEqual(result, None)

    def test_with_one_uri(self):
        target = self._makeOne()
        marker = object()
        target.add("top", "/")
        result = target.lookup("/")

        self.assertEqual(result.name, "top")

    def test_with_two_uri(self):
        target = self._makeOne()
        marker = object()
        target.add("user", "/user")
        target.add("top", "/")
        result = target.lookup("/")

        self.assertEqual(result.name, "top")

    def test_with_retain(self):
        target = self._makeOne()
        marker = object()
        from .uritemplate import URITemplateFormatException 
        try:
            target.add("user", "/user*")
            self.fail()
        except URITemplateFormatException:
            pass

    def test_with_retain2(self):
        target = self._makeOne()
        marker = object()
        target.add("user", "/user/*")
        # precondition
        # self.assertTrue(target.patterns['user'].match("/user/a"))
        result = target.lookup("/user/a")

        self.assertEqual(result.name, "user")

    def test_generate(self):
        target = self._makeOne()
        marker = object()
        target.add("user", "/user")

        result = target.generate("user")
        self.assertEqual(result, '/user')


class URLGeneratorTests(unittest.TestCase):
    def _getTarget(self):
        from .urldispatcher import URLGenerator
        return URLGenerator

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_generate(self):
        environ = {'SCRIPT_NAME': '/test_app/', 
            'wsgi.url_scheme': 'http',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80'}
        class DummyMapper(object):
            def generate(self, *args, **kwargs):
                return 'generated_url'

        dummy_mapper = DummyMapper()
        target = self._makeOne(environ, dummy_mapper)
        result = target.generate('users', user_id='aodag')
        self.assertEqual(result, 'http://localhost/test_app/generated_url')

class URLDispatcherTests(unittest.TestCase):

    def _getTarget(self):
        from .urldispatcher import URLDispatcher
        return URLDispatcher

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def _makeEnv(self, path_info, script_name):
        return testing.make_env(path_info, script_name)

    def test_make(self):
        target = self._getTarget()
        dummy = object()
        result = target(urlmapper=dummy)
        self.assertEqual(result.urlmapper, dummy)

    def test_add_subroute(self):
        target = self._makeOne(prefix='/root')
        result = target.add_subroute('/sub')

        self.assertEqual(result.urlmapper, target.urlmapper)
        self.assertEqual(result.prefix, '/root/sub')

    def test_empty(self):

        def app(environ, start_response):
            return environ

        target = self._makeOne()
        target.add_url("top", "", app)
        environ = self._makeEnv("", "")

        result = target(environ, None)
        self.assertEqual(result['PATH_INFO'], '') 
        self.assertEqual(result['SCRIPT_NAME'], '')
        self.assertEqual(result['wsgiorg.routing_args'], ([], {}))
        self.assertEqual(result['webdispatch.urlmapper'], target.urlmapper)

    def test_one(self):

        def app(environ, start_response):
            return environ

        target = self._makeOne()
        target.add_url("top", "/{var1}", app)
        environ = self._makeEnv("/a", "a")

        result = target(environ, None)
        self.assertEqual(result['PATH_INFO'], '') 
        self.assertEqual(result['SCRIPT_NAME'], 'a/a')
        self.assertEqual(result['wsgiorg.routing_args'], ([], {'var1': 'a'}))

    def test_notfound(self):
        target = self._makeOne()
        environ = self._makeEnv("", "")
        called = []
        def start_response(status, headers):
            called.append((status, headers))
        result = target(environ, start_response)
        self.assertEqual(result, [b"Not found"])
        

    def test_add_url(self):
        target = self._makeOne()
        marker = object()
        target.add_url('top', '/', marker)
        self.assertEqual(target.urlmapper.patterns['top'].pattern, '/')

class PatternToRegexTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from .uritemplate import pattern_to_regex
        return pattern_to_regex(*args, **kwargs)

    def test_empty(self):
        pattern = ""
        result = self._callFUT(pattern)

        self.assertEqual(result, "^$")

    def test_regex_meta_chas(self):
        pattern = "{name}.{suffix}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<name>\w+)\.(?P<suffix>\w+)$")

    def test_open_path(self):
        pattern = "hoge*"
        result = self._callFUT(pattern)

        self.assertEqual(result, "^hoge")

    def test_close_path(self):
        pattern = "hoge"
        result = self._callFUT(pattern)

        self.assertEqual(result, "^hoge$")

    def test_one_var(self):
        pattern = "{var1}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<var1>\w+)$")

    def test_two_vars(self):
        pattern = "{var1}{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<var1>\w+)(?P<var2>\w+)$")

    def test_vars(self):
        pattern = "/{var1}/{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^/(?P<var1>\w+)/(?P<var2>\w+)$")

class URITemplateTests(unittest.TestCase):
    def _getTarget(self):
        from .uritemplate import URITemplate
        return URITemplate

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_match_empty(self):
        path = ""
        target = self._makeOne(path)

        result = target.match(path)

        self.assertEqual(result.matchdict, dict())
        self.assertEqual(result.matchlength, 0)

    def test_wildcard(self):
        path = "hoge/{var1}/*"
        target = self._makeOne(path)
        result = target.match("hoge/egg/bacon")

        self.assertEqual(result.matchdict, dict(var1="egg"))
        self.assertEqual(result.matchlength, 9)

    def test_match_no_match(self):
        path = "hoge/{vars}"
        target = self._makeOne(path)
        result = target.match("spam/egg")

        self.assertEqual(result, None)

    def test_match_match_one(self):
        path = "{var1}"
        target = self._makeOne(path)
        result = target.match("a")

        self.assertEqual(result.matchdict, dict(var1="a"))
        self.assertEqual(result.matchlength, 1)

    def test_match_match_many(self):
        path = "{var1}/users/{var2}"
        target = self._makeOne(path)
        result = target.match("a/users/egg")

        self.assertEqual(result.matchdict, dict(var1="a", var2="egg"))

    def test_substitue(self):
        path = "{var1}/users/{var2}"
        target = self._makeOne(path)
        result = target.substitute(dict(var1="x", var2="y"))

        self.assertEqual(result, "x/users/y")

class MethodDispatcherTests(unittest.TestCase):
    def _getTarget(self):
        from .methoddispatcher import MethodDispatcher
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

class ActionDispatcherTests(unittest.TestCase):
    def _getTarget(self):
        from .methoddispatcher import ActionDispatcher
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
        app.register_app('test_app', lambda environ, start_response: ['got action'])
        routing_args = [(), {'action': 'test_app'}]
        environ = self._setup_environ(**{'wsgiorg.routing_args': routing_args})
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, ["got action"])

    def test_not_found(self):
        app = self._makeOne()
        app.register_app('test_app', lambda environ, start_response: ['got action'])
        routing_args = [(), {'action': 'no_app'}]
        environ = self._setup_environ(**{'wsgiorg.routing_args': routing_args})
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(start_response.status, '404 Not Found')
        self.assertEqual(result, [b"Not Found ", b"http://127.0.0.1/"])

class URLMapperMixinTests(unittest.TestCase):
    def _getTarget(self):
        from .mixins import URLMapperMixin
        return URLMapperMixin

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_generate_url(self):
        target = self._makeOne()
        dummy_generator = testing.DummyURLGenerator('generated')
        target.environ = {'webdispatch.urlgenerator': dummy_generator}
        result = target.generate_url('a', v1='1', v2='2')

        self.assertEqual(result, 'generated')
        self.assertEqual(dummy_generator.called, ('generate', 'a', {'v1': '1', 'v2': '2'}))


class PasteTests(unittest.TestCase):

    def _makeEnv(self, path_info, script_name):
        return testing.make_env(path_info, script_name)

    def _callFUT(self, *args, **kwargs):
        from .paster import make_urldispatch_application
        return make_urldispatch_application(*args, **kwargs)

    def assertResponseBody(self, app, path, expected):
        environ = self._makeEnv(path, '')
        start_response = testing.DummyStartResponse()
        result = app(environ, start_response)
        self.assertEqual(result, expected)

    def test_it(self):
        global_conf = {}
        settings = {"patterns": """\
        / = webdispatch.testing:greeting
        /bye = webdispatch.testing:bye"""}

        application = self._callFUT(global_conf, **settings)
        self.assertResponseBody(application, '/', [b'Hello'])
        self.assertResponseBody(application, '/bye', [b'bye'])
