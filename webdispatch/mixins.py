""" useful mixin classes
"""


class URLMapperMixin(object):
    """ mixin to add :meth:`generate_url` method.
    """
    def generate_url(self, name, **kwargs):
        """ generate url with urlgenerator used by urldispatch"""
        mapper = self.environ['webdispatch.urlgenerator']
        return mapper.generate(name, **kwargs)
