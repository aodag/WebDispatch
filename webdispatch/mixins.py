""" useful mixin classes
"""
from typing import Dict, Any  # noqa pylint: disable=unused-import
from .urldispatcher import URLGenerator


class URLMapperMixin(object):
    """ mixin to add :meth:`generate_url` method.
    """

    environ = {}  # type: Dict[str, Any]

    def generate_url(self, name: str, **kwargs) -> str:
        """ generate url with urlgenerator used by urldispatch"""
        return self.urlmapper.generate(name, **kwargs)

    @property
    def urlmapper(self) -> URLGenerator:
        """ get urlmapper object from wsgi environ """
        return self.environ["webdispatch.urlgenerator"]
