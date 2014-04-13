""" test for webdispatch.mixins"""
import unittest
from webdispatch import testing


class URLMapperMixinTests(unittest.TestCase):
    def _getTarget(self):
        from webdispatch.mixins import URLMapperMixin
        return URLMapperMixin

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_generate_url(self):
        target = self._makeOne()
        dummy_generator = testing.DummyURLGenerator('generated')
        target.environ = {'webdispatch.urlgenerator': dummy_generator}
        result = target.generate_url('a', v1='1', v2='2')

        self.assertEqual(result, 'generated')
        self.assertEqual(dummy_generator.called,
                         ('generate', 'a', {'v1': '1', 'v2': '2'}))
