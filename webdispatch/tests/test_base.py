""" tests for webdispatch.base """
import mock
from testfixtures import compare


class TestDispatchBase(object):
    """ test for webdispatch.base.DispatchBase """

    @staticmethod
    def _get_target():
        """ get class under test """
        from webdispatch.base import DispatchBase

        return DispatchBase

    def _make_one(self, *args, **kwargs):
        """ create object under test"""
        return self._get_target()(*args, **kwargs)

    def test_init(self):
        """ init no app and no environ"""

        result = self._make_one()

        compare(result.applications, {})
        compare(result.extra_environ, {})

    def test_init_apps(self):
        """ init with app and no environ"""

        testing_app = object()
        result = self._make_one(applications={"testing": testing_app})

        compare(result.applications, {"testing": testing_app})
        compare(result.extra_environ, {})

    def test_init_env(self):
        """ init with app and no environ"""

        environ = {"test_value": 1}
        result = self._make_one(extra_environ=environ)

        compare(result.applications, {})
        compare(result.extra_environ, {"test_value": 1})

    def test_not_found(self):
        """ init with app and no environ"""

        marker = object()
        target = self._make_one()
        target.detect_view_name = lambda environ: None
        target.on_view_not_found = lambda environ, start_response: marker
        start_response = mock.Mock()
        result = target({}, start_response)

        compare(result, marker)
