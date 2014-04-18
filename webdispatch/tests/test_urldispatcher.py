"""
tests for webdispatch.urldispatcher
"""
import collections
import mock
from testfixtures import compare, Comparison as C
from webdispatch.testing import setup_environ


class TestURLMapper(object):
    """ tests for webdispatch.urldispatcher.URLMapper """
    @staticmethod
    def _get_target():
        """ get class under test """
        from webdispatch.urldispatcher import URLMapper
        return URLMapper

    def _make_one(self, *args, **kwargs):
        """ create object under test """
        return self._get_target()(*args, **kwargs)

    def test_init(self):
        """ test create object """
        converters = {
            'int': int,
            'str': str,
            'float': float,
        }
        target = self._make_one(converters)

        compare(target, C(self._get_target(),
                          patterns=collections.OrderedDict(),
                          converters=converters))

    def test_add(self):
        """ test add url """
        from webdispatch.uritemplate import URITemplate
        converters = {
            'int': int,
            'str': str,
            'float': float,
        }
        pattern = '/{v1}/{v2:int}'

        target = self._make_one(converters)
        target.add('testing-route', pattern)

        compare(target.patterns,
                {'testing-route': C(URITemplate,
                                    converters={'v1': str,
                                                'v2': int},
                                    pattern=pattern,
                                    strict=False)})

    def test_lookup_none(self):
        """ test looking up route no registered routes"""
        target = self._make_one()
        result = target.lookup('a')
        compare(result, None)

    def test_lookup(self):
        """ test looking up basic usage """
        target = self._make_one()
        target.add('testing-route', 'a')
        result = target.lookup('a')
        compare(result, {'name': 'testing-route',
                         'matchdict': {},
                         'matchlength': 1})

    def test_generate(self):
        """ test generating url """
        target = self._make_one()
        target.add('testing-route', 'a/{v1}')

        result = target.generate('testing-route', v1='b')
        compare(result, 'a/b')


class TestURLGenerator(object):
    """ test for webdispatch.urldispatcher.URLGenerator """
    @staticmethod
    def _get_target():
        """ get class under test """
        from webdispatch.urldispatcher import URLGenerator
        return URLGenerator

    def _make_one(self, *args, **kwargs):
        """ create object under test """
        return self._get_target()(*args, **kwargs)

    def test_init(self):
        """ test create object """
        environ = setup_environ()
        urlmapper = object()
        target = self._make_one(environ, urlmapper)

        compare(target.environ, environ)
        compare(target.urlmapper, urlmapper)
        compare(target.application_uri, 'http://127.0.0.1/')

    def test_generate(self):
        """ test generating url """
        environ = setup_environ()
        urlmapper = mock.Mock()
        urlmapper.generate.return_value = 'testing-route-url'
        target = self._make_one(environ, urlmapper)

        result = target.generate('testing-route', v1="a")

        compare(result, 'http://127.0.0.1/testing-route-url')


class TestURLDispatcher(object):
    """ tests for webdispatch.urldispatcher.URLDispatcher """
    @staticmethod
    def _get_target():
        """ get class under test """
        from webdispatch.urldispatcher import URLDispatcher
        return URLDispatcher

    def _make_one(self, *args, **kwargs):
        """ create object under test """
        return self._get_target()(*args, **kwargs)

    def test_init(self):
        """ test init """
        target = self._make_one()
        compare(target, C(self._get_target()))

    def test_init_mapper(self):
        """ test init with cutome mapper"""
        mapper = object()
        target = self._make_one(urlmapper=mapper)
        compare(target, C(self._get_target()))
        compare(target.urlmapper, mapper)

    def test_add_url(self):
        """ test add_url"""
        mapper = mock.Mock()
        target = self._make_one(urlmapper=mapper)
        app = object()
        target.add_url('testing-route', 'a/b', app)

        mapper.add.assert_called_with('testing-route', 'a/b')

    def test_subroute(self):
        mapper = object()
        target = self._make_one(urlmapper=mapper,
                                extra_environ={'testing': 'e'})
        result = target.add_subroute('prefix/a/b')

        compare(result, C(self._get_target(),
                          urlmapper=mapper,
                          prefix='prefix/a/b',
                          applications={},
                          extra_environ={'testing': 'e'}))

    def test_detect_view_name(self):
        target = self._make_one()
        environ = setup_environ()
        result = target.detect_view_name(environ)

        compare(result, None)

    def test_on_view_not_found(self):
        target = self._make_one()
        environ = setup_environ()
        start_response = mock.Mock()
        result = target(environ, start_response)

        compare(result, [b'Not found'])
        start_response.assert_called_with(
            '404 Not Found', [('Content-type', 'text/plain')])
