import unittest

class URLMapperTests(unittest.TestCase):
    def _getTarget(self):
        from .dispatcher import URLMapper
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
        target.add("top", "/", marker)
        result = target.lookup("/")

        self.assertEqual(result[0].name, "top")
        self.assertEqual(result[1], marker)

    def test_with_two_uri(self):
        target = self._makeOne()
        marker = object()
        target.add("user", "/user", marker)
        target.add("top", "/", marker)
        result = target.lookup("/")

        self.assertEqual(result[0].name, "top")
        self.assertEqual(result[1], marker)

    def test_with_retain(self):
        target = self._makeOne()
        marker = object()
        target.add("user", "/user*", marker)
        result = target.lookup("/users")

        self.assertEqual(result, None)

    def test_generate(self):
        target = self._makeOne()
        marker = object()
        target.add('users', "/users/{user_id}", marker)
        result = target.generate('users', user_id='aodag')
        self.assertEqual(result, '/users/aodag')

class DispatcherTests(unittest.TestCase):

    def _getTarget(self):
        from .dispatcher import Dispatcher
        return Dispatcher

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def _makeEnv(self, path_info, script_name):
        return {
            "PATH_INFO": path_info,
            "SCRIPT_NAME": script_name,
        }

    def test_empty(self):

        def app(environ, start_response):
            return environ

        target = self._makeOne([("top", "", app)])
        environ = self._makeEnv("", "")

        result = target(environ, None)
        self.assertEqual(result['PATH_INFO'], '') 
        self.assertEqual(result['SCRIPT_NAME'], '')
        self.assertEqual(result['wsgiorg.routing_args'], ([], {}))
        self.assertEqual(result['webdispatch.urlmapper'], target.urlmapper)

    def test_one(self):

        def app(environ, start_response):
            return environ

        target = self._makeOne([("top", "/{var1}", app)])
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
        self.assertEqual(result, ["Not found"])
        

    def test_add_url(self):
        target = self._makeOne()
        marker = object()
        target.add_url('top', '/', marker)
        self.assertEqual(target.urlmapper.patterns['top'][0].pattern, '/')
        self.assertEqual(target.urlmapper.patterns['top'][1], marker)

class PatternToRegexTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from .uritemplate import pattern_to_regex
        return pattern_to_regex(*args, **kwargs)

    def test_empty(self):
        pattern = ""
        result = self._callFUT(pattern)

        self.assertEqual(result, "^$")

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

