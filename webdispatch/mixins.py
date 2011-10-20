class URLMapperMixin(object):
    """ mixin to add :meth:`generate_url` method.
    """
    def generate_url(self, name, **kwargs):
        mapper = self.environ['webdispatch.urlgenerator']
        return mapper.generate(name, **kwargs)
