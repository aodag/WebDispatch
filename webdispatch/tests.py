import unittest

class TestIt(unittest.TestCase):

    def test_it(self):
        from .dispatcher import RegexDispatch

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

        self.assertEqual(result, r"^(?P<var1>\w+)$")

    def test_two_vars(self):
        pattern = "{var1}{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^(?P<var1>\w+)(?P<var2>\w+)$")

    def test_vars(self):
        pattern = "/{var1}/{var2}"
        result = self._callFUT(pattern)

        self.assertEqual(result, r"^/(?P<var1>\w+)/(?P<var2>\w+)$")
