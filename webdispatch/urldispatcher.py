""" urldispatcher

"""
from collections import OrderedDict
from wsgiref.util import application_uri

from .uritemplate import URITemplate
from .base import DispatchBase


class URLMapper(object):
    """ find application matched url pattern.
    """

    def __init__(self, converters=None):
        self.patterns = OrderedDict()
        self.converters = converters

    def add(self, name, pattern):
        """ add url pattern for name
        """
        self.patterns[name] = URITemplate(
            pattern, converters=self.converters)

    def lookup(self, path_info):
        """ lookup url match for path_info
        """
        for name, pattern in self.patterns.items():
            match = pattern.match(path_info)
            if match is None:
                continue
            match["name"] = name
            return match

    def generate(self, name, **kwargs):
        """ generate url for named url pattern with kwargs
        """
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
        """ generate full qualified url for named url pattern with kwargs
        """
        path = self.urlmapper.generate(name, **kwargs)
        return self.make_full_qualified_url(path)

    def make_full_qualified_url(self, path):
        """ append application url to path"""
        return self.application_uri.rstrip('/') + '/' + path.lstrip('/')


class URLDispatcher(DispatchBase):
    """ dispatch applications with url patterns.
    """

    def __init__(self,
                 applications=None,
                 extra_environ=None,
                 **kwargs):
        super(URLDispatcher, self).__init__(
            applications=applications,
            extra_environ=extra_environ)
        converters = kwargs.get('converters')
        if 'urlmapper' in kwargs:
            self.urlmapper = kwargs['urlmapper']
        else:
            self.urlmapper = URLMapper(converters=converters)
        self.prefix = kwargs.get('prefix', '')

    def add_url(self, name, pattern, application):
        """ add url pattern dispatching to application"""
        self.urlmapper.add(name, self.prefix + pattern)
        self.register_app(name, application)

    def add_subroute(self, pattern):
        """ create new URLDispatcher routed by pattern """
        return URLDispatcher(
            urlmapper=self.urlmapper,
            prefix=self.prefix + pattern,
            applications=self.applications,
            extra_environ=self.extra_environ)

    def detect_view_name(self, environ):
        """ detect view name from environ """
        script_name = environ.get('SCRIPT_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        match = self.urlmapper.lookup(path_info)
        if match is None:
            return None

        extra_path_info = path_info[match["matchlength"]:]
        pos_args = []
        named_args = match["matchdict"]
        cur_pos, cur_named = environ.get('wsgiorg.routing_args', ((), {}))
        new_pos = list(cur_pos) + list(pos_args)
        new_named = cur_named.copy()
        new_named.update(named_args)
        environ['wsgiorg.routing_args'] = (new_pos, new_named)
        environ['webdispatch.urlmapper'] = self.urlmapper
        urlgenerator = URLGenerator(environ, self.urlmapper)
        environ['webdispatch.urlgenerator'] = urlgenerator
        environ['SCRIPT_NAME'] = script_name + path_info[:match["matchlength"]]
        environ['PATH_INFO'] = extra_path_info

        return match["name"]

    def on_view_not_found(self, environ, start_response):
        """ called when views not found"""
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not found']
