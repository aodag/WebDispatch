""" test for webdispatch.mixins"""
import mock
from testfixtures import compare


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
        dummy_generator = mock.Mock()
        dummy_generator.generate.return_value = 'generated'
        target.environ = {'webdispatch.urlgenerator': dummy_generator}
        result = target.generate_url('a', v1='1', v2='2')

        compare(result, 'generated')
        dummy_generator.generate.assert_called_with(
            'a', v1='1', v2='2')

    def test_urlmapper(self):
        """ test urlmapper property """
        target = self._make_one()
        dummy_generator = object()
        target.environ = {'webdispatch.urlgenerator': dummy_generator}
        result = target.urlmapper

        compare(result, dummy_generator)
