""" useful mixin classes
"""


class URLMapperMixin(object):
    """ mixin to add :meth:`generate_url` method.
    """
    def generate_url(self, name, **kwargs):
        """ generate url with urlgenerator used by urldispatch"""
        return self.urlmapper.generate(name, **kwargs)

    @property
    def urlmapper(self):
        """ get urlmapper object from wsgi environ """
        return self.environ['webdispatch.urlgenerator']
