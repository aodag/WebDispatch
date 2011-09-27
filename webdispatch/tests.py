import unittest

class DispatcherTests(unittest.TestCase):

    def _getTarget(self):
        from .dispatcher import RegexDispatch
        return RegexDispatch

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_empty(self):

        def app(environ, start_response):
            return environ

        target = self._makeOne([("", app)])
        environ = {
            'PATH_INFO': "",
            'SCRIPT_NAME': "",
        }

        result = target(environ, None)
        self.assertEqual(result, 
            {'PATH_INFO': '', 
            'SCRIPT_NAME': '', 
            'wsgiorg.routing_args':([], {})})

    def test_one(self):

        def app(environ, start_response):
            return environ

        target = self._makeOne([("/{var1}", app)])
        environ = {
            'PATH_INFO': "/a",
            'SCRIPT_NAME': "a",
        }

        result = target(environ, None)
        self.assertEqual(result, 
            {'PATH_INFO': '', 
            'SCRIPT_NAME': 'a/a', 
            'wsgiorg.routing_args':([], {'var1': 'a'})})

class PatternToRegexTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from .uritemplate import pattern_to_regex
        return pattern_to_regex(*args, **kwargs)

    def test_empty(self):
        pattern = ""
        result = self._callFUT(pattern)

        self.assertEqual(result, "^$")

    def test_one_var(self):
        pattern = "{var1}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<var1>[^:,?#\[\]@!$&'\(\)\*\+,;=]+?)$")

    def test_two_vars(self):
        pattern = "{var1}{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<var1>[^:,?#\[\]@!$&'\(\)\*\+,;=]+?)(?P<var2>[^:,?#\[\]@!$&'\(\)\*\+,;=]+?)$")

    def test_vars(self):
        pattern = "/{var1}/{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^/(?P<var1>[^:,?#\[\]@!$&'\(\)\*\+,;=]+?)/(?P<var2>[^:,?#\[\]@!$&'\(\)\*\+,;=]+?)$")

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

    def test_match_reserved(self):
        path = "{+var1}/a/{+var2}/a"
        target = self._makeOne(path)
        result = target.match("abcdea/a/a/a")

        self.assertEqual(result.matchdict, dict(var1="abcdea", var2="a"))
        self.assertEqual(result.matchlength, 12)
