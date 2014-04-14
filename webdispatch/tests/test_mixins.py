""" test for webdispatch.mixins"""
from testfixtures import compare
from webdispatch import testing


class TestURLMapperMixin(object):
    """ test for URLMapperMixin"""

    @staticmethod
    def _get_target():
        """ get class under test """
        from webdispatch.mixins import URLMapperMixin
        return URLMapperMixin

    def _make_one(self, *args, **kwargs):
        """ generate object under test """
        return self._get_target()(*args, **kwargs)

    def test_generate_url(self):
        """ test generate_url """
        target = self._make_one()
        dummy_generator = testing.DummyURLGenerator('generated')
        target.environ = {'webdispatch.urlgenerator': dummy_generator}
        result = target.generate_url('a', v1='1', v2='2')

        compare(result, 'generated')
        compare(dummy_generator.called,
                ('generate', 'a', {'v1': '1', 'v2': '2'}))
