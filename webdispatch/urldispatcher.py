from .uritemplate import URITemplate
from .util import application_uri
from .base import DispatchBase

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

class URLMapper(object):
    """ find application matched url pattern.
    """

    def __init__(self):
        self.patterns = OrderedDict()

    def add(self, name, pattern):
        self.patterns[name] = URITemplate(pattern)

    def lookup(self, path_info):
        for name, pattern in self.patterns.items():
            match = pattern.match(path_info)
            if match is None:
                continue
            match.name = name
            return match

    def generate(self, name, **kwargs):
        template = self.patterns[name]
        return template.substitute(kwargs)

class URLGenerator(object):
    """ generate url form parameters and url patterns.
    """

    def __init__(self, environ, urlmapper):
        self.environ = environ
        self.urlmapper = urlmapper
        self.application_uri = application_uri(environ)

    def generate(self, name, **kwargs):
        path = self.urlmapper.generate(name, **kwargs)

        return self.application_uri + path

class URLDispatcher(DispatchBase):
    """ dispatch applications with url patterns.
    """

    def __init__(self, urlmapper=None, prefix='', applications=None):
        super(URLDispatcher, self).__init__(applications=applications)
        if urlmapper is None:
            self.urlmapper = URLMapper()
        else:
            self.urlmapper = urlmapper

        self.prefix = prefix

    def add_url(self, name, pattern, application):
        self.urlmapper.add(name, self.prefix + pattern)
        self.register_app(name, application)

    def add_subroute(self, pattern):
        return URLDispatcher(urlmapper=self.urlmapper,
            prefix=self.prefix + pattern,
            applications=self.applications)

    def detect_view_name(self, environ):
        script_name = environ.get('SCRIPT_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        match = self.urlmapper.lookup(path_info)
        if match is None:
            return None

        extra_path_info = path_info[match.matchlength:]
        pos_args = []
        named_args = match.matchdict
        cur_pos, cur_named = environ.get('wsgiorg.routing_args', ((), {}))
        new_pos = list(cur_pos) + list(pos_args)
        new_named = cur_named.copy()
        new_named.update(named_args)
        environ['wsgiorg.routing_args'] = (new_pos, new_named)
        environ['webdispatch.urlmapper'] = self.urlmapper
        environ['webdispatch.urlgenerator'] = URLGenerator(environ, self.urlmapper)
        environ['SCRIPT_NAME'] = script_name + path_info[:match.matchlength]
        environ['PATH_INFO'] = extra_path_info

        return match.name

    def on_view_not_found(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return ['Not found']
