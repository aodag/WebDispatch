""" tests for webdispatch.uritemplate """

from testfixtures import compare, ShouldRaise


class TestPatternToRegex(object):
    """ test webdispatch.uritemplate.pattern_to_regex"""

    @staticmethod
    def _call_fut(*args, **kwargs):
        """ call function under test """
        from webdispatch.uritemplate import pattern_to_regex
        return pattern_to_regex(*args, **kwargs)

    def test_empty(self):
        """ test converting empty string """
        pattern = ""
        result = self._call_fut(pattern)

        compare(result, "^$")

    def test_regex_meta_chars(self):
        """ test converting included meta characters """
        pattern = "{name}.{suffix}"
        result = self._call_fut(pattern)

        compare(result, r"^(?P<name>[\w-]+)\.(?P<suffix>[\w-]+)$")

    def test_open_path(self):
        """ test converting having open suffix"""
        pattern = "hoge*"
        result = self._call_fut(pattern)

        compare(result, "^hoge")

    def test_close_path(self):
        """ test converting not having open suffix"""
        pattern = "hoge"
        result = self._call_fut(pattern)

        compare(result, "^hoge$")

    def test_one_var(self):
        """ test converting including one var"""
        pattern = "{var1}"
        result = self._call_fut(pattern)

        compare(result, r"^(?P<var1>[\w-]+)$")

    def test_two_vars(self):
        """ test converting including two vers"""
        pattern = "{var1}{var2}"
        result = self._call_fut(pattern)

        compare(result, r"^(?P<var1>[\w-]+)(?P<var2>[\w-]+)$")

    def test_vars(self):
        """ test converting separated two vars """
        pattern = "/{var1}/{var2}"
        result = self._call_fut(pattern)

        compare(result, r"^/(?P<var1>[\w-]+)/(?P<var2>[\w-]+)$")


class TestURITemplate(object):
    """ test for webdispatch.uritemplate.URITemplate """

    @staticmethod
    def _get_target():
        """ get class under test"""
        from webdispatch.uritemplate import URITemplate
        return URITemplate

    def _make_one(self, *args, **kwargs):
        """ create object under test"""
        return self._get_target()(*args, **kwargs)

    def test_bad_format(self):
        """ test bad format template"""
        from webdispatch.uritemplate import URITemplateFormatException
        path = "a*"
        with ShouldRaise(URITemplateFormatException):
            self._make_one(path)

    def test_match_empty(self):
        """ test matching empty path """
        path = ""
        target = self._make_one(path)

        result = target.match(path)

        compare(result["matchdict"], dict())
        compare(result["matchlength"], 0)

    def test_wildcard(self):
        """ test matching pattern including wildcard"""
        path = "hoge/{var1}/*"
        target = self._make_one(path)
        result = target.match("hoge/egg/bacon")

        compare(result["matchdict"], dict(var1="egg"))
        compare(result["matchlength"], 9)

    def test_match_no_match(self):
        """ test no mathing"""
        path = "hoge/{vars}"
        target = self._make_one(path)
        result = target.match("spam/egg")

        compare(result, None)

    def test_match_match_one(self):
        """ test matching a character """
        path = "{var1}"
        target = self._make_one(path)
        result = target.match("a")

        compare(result["matchdict"], dict(var1="a"))
        compare(result["matchlength"], 1)

    def test_match_match_complex_word(self):
        """ test matching a string"""
        path = "{var1}"
        target = self._make_one(path)
        result = target.match("abc")

        compare(result["matchdict"], dict(var1="abc"))

    def test_match_match_many(self):
        """ test matching pattern including two vars """
        path = "{var1}/users/{var2}"
        target = self._make_one(path)
        result = target.match("a/users/egg")

        compare(result["matchdict"], dict(var1="a", var2="egg"))

    def test_substitue(self):
        """ test subtituting vars to pattern """
        path = "{var1}/users/{var2}"
        target = self._make_one(path)
        result = target.substitute(dict(var1="x", var2="y"))

        compare(result, "x/users/y")
