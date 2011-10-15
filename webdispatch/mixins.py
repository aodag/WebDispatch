class URLMapperMixin(object):
    def generate_url(self, name, **kwargs):
        mapper = self.environ['webdispatch.urlgenerator']
        return mapper.generate(name, **kwargs)
