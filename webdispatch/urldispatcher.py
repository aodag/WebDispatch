from .uritemplate import URITemplate
from .util import application_uri

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

class URLMapper(object):
    def __init__(self):
        self.patterns = OrderedDict()

    def add(self, name, pattern, application):
        self.patterns[name] = (URITemplate(pattern), application)

    def lookup(self, path_info):
        for name, pattern in self.patterns.items():
            regex, application = pattern
            match = regex.match(path_info)
            if match is None:
                continue
            match.name = name
            extra_path_info = path_info[match.matchlength:]
            if extra_path_info and not extra_path_info.startswith('/'):
                continue
            return match, application

    def generate(self, name, **kwargs):
        template, _ = self.patterns[name]
        return template.substitute(kwargs)

class URLGenerator(object):
    def __init__(self, environ, urlmapper):
        self.environ = environ
        self.urlmapper = urlmapper
        self.application_uri = application_uri(environ)

    @property
    def script_name(self):
        return self.environ.get('SCRIPT_NAME', '')

    def generate(self, name, **kwargs):
        path = self.urlmapper.generate(name, **kwargs)

        return self.application_uri + path

class URLDispatcher(object):

    def __init__(self, applications=None, urlmapper=None, prefix=''):
        if urlmapper is None:
            self.urlmapper = URLMapper()
        else:
            self.urlmapper = urlmapper

        self.prefix = prefix

        if applications is not None:
            for name, pattern, application in applications:
                self.urlmapper.add(name, pattern, application)

    def add_url(self, name, pattern, application):
        self.urlmapper.add(name, self.prefix + pattern, application)

    def add_subroute(self, pattern):
        return URLDispatcher(urlmapper=self.urlmapper,
            prefix=self.prefix + pattern)

    def __call__(self, environ, start_response):
        script_name = environ.get('SCRIPT_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        matches = self.urlmapper.lookup(path_info)
        if matches is None:
            return self.not_found(environ, start_response)
        match, application = matches

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
        return application(environ, start_response)

    def not_found(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return ['Not found']
