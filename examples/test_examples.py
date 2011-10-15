import webtest
import unittest

class HelloTests(unittest.TestCase):
    def _getAUT(self):
        from hello import app
        return webtest.TestApp(app)

    def test_it(self):
        app = self._getAUT()
        res = app.get('/')
        self.assertTrue('Hello' in res)

        res = app.get('/hello/aodag')
        self.assertTrue('Hello aodag' in res)

class SubroutingTests(unittest.TestCase):

    def _getAUT(self):
        from subrouting import app
        return webtest.TestApp(app)

    def test_it(self):
        app = self._getAUT()
        res = app.get('/')
        self.assertTrue('/' in res)

        res = app.get('/sub')
        self.assertTrue('/sub' in res)

        res = app.get('/sub/x')
        self.assertTrue('/sub/x' in res)

    def test_generate(self):
        app = self._getAUT()
        res = app.get('/gen')
        self.assertTrue('/sub/x' in res)

        res = app.get('/sub/gen')
        self.assertTrue('/sub/x' in res)
