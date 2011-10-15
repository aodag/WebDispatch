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
