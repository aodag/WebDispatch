""" tests for webdispatch.uritemplate """

import unittest


class PatternToRegexTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from webdispatch.uritemplate import pattern_to_regex
        return pattern_to_regex(*args, **kwargs)

    def test_empty(self):
        pattern = ""
        result = self._callFUT(pattern)

        self.assertEqual(result, "^$")

    def test_regex_meta_chas(self):
        pattern = "{name}.{suffix}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<name>[\w-]+)\.(?P<suffix>[\w-]+)$")

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

        self.assertEqual(result, r"^(?P<var1>[\w-]+)$")

    def test_two_vars(self):
        pattern = "{var1}{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<var1>[\w-]+)(?P<var2>[\w-]+)$")

    def test_vars(self):
        pattern = "/{var1}/{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^/(?P<var1>[\w-]+)/(?P<var2>[\w-]+)$")


class URITemplateTests(unittest.TestCase):
    def _getTarget(self):
        from webdispatch.uritemplate import URITemplate
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

    def test_match_match_complex_word(self):
        path = "{var1}"
        target = self._makeOne(path)
        result = target.match("abc")

        self.assertEqual(result.matchdict, dict(var1="abc"))

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
