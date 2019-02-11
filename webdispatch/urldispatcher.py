""" urldispatcher

"""
from collections import OrderedDict
from wsgiref.util import application_uri
from typing import Any, Callable, Dict, List, Optional, Tuple, Iterable  # noqa
from .uritemplate import URITemplate, MatchResult
from .base import DispatchBase


class URLMapper(object):
    """ find application matched url pattern.
    """

    def __init__(self, converters: Dict[str, Callable] = None) -> None:
        self.patterns = OrderedDict()  # type: Dict[str, URITemplate]
        self.converters = converters

    def add(self, name: str, pattern: str) -> None:
        """ add url pattern for name
        """
        self.patterns[name] = URITemplate(pattern, converters=self.converters)

    def lookup(self, path_info: str) -> Optional[MatchResult]:
        """ lookup url match for path_info
        """
        for name, pattern in self.patterns.items():
            match = pattern.match(path_info)
            if match is None:
                continue
            match.name = name
            return match
        return None

    def generate(self, name: str, **kwargs: Dict[str, str]) -> str:
        """ generate url for named url pattern with kwargs
        """
        template = self.patterns[name]
        return template.substitute(kwargs)


class URLGenerator(object):
    """ generate url form parameters and url patterns.
    """

    def __init__(self, environ: Dict[str, Any], urlmapper: URLMapper) -> None:
        self.environ = environ
        self.urlmapper = urlmapper
        self.application_uri = application_uri(environ)

    def generate(self, name: str, **kwargs):
        """ generate full qualified url for named url pattern with kwargs
        """
        path = self.urlmapper.generate(name, **kwargs)
        return self.make_full_qualified_url(path)

    def make_full_qualified_url(self, path: str) -> str:
        """ append application url to path"""
        return self.application_uri.rstrip("/") + "/" + path.lstrip("/")


class URLDispatcher(DispatchBase):
    """ dispatch applications with url patterns.
    """

    def __init__(
        self,
        *,
        applications: Dict[str, Callable] = None,
        extra_environ: Dict[str, Any] = None,
        converters: Dict[str, Callable] = None,
        urlmapper: URLMapper = None,
        prefix: str = ""
    ) -> None:
        super(URLDispatcher, self).__init__(
            applications=applications, extra_environ=extra_environ
        )
        if urlmapper:
            self.urlmapper = urlmapper
        else:
            self.urlmapper = URLMapper(converters=converters)
        self.prefix = prefix

    def add_url(self, name: str, pattern: str, application: Callable) -> None:
        """ add url pattern dispatching to application"""
        self.urlmapper.add(name, self.prefix + pattern)
        self.register_app(name, application)

    def add_subroute(self, pattern: str) -> "URLDispatcher":
        """ create new URLDispatcher routed by pattern """
        return URLDispatcher(
            urlmapper=self.urlmapper,
            prefix=self.prefix + pattern,
            applications=self.applications,
            extra_environ=self.extra_environ,
        )

    def detect_view_name(self, environ: Dict[str, Any]) -> Optional[str]:
        """ detect view name from environ """
        script_name = environ.get("SCRIPT_NAME", "")
        path_info = environ.get("PATH_INFO", "")
        match = self.urlmapper.lookup(path_info)
        if match is None:
            return None

        splited = match.split_path_info(path_info)
        extra_path_info = splited[1]
        pos_args = []  # type: List[str]

        routing_args = environ.get("wsgiorg.routing_args", ((), {}))
        (cur_pos, cur_named) = routing_args
        new_pos = list(cur_pos) + list(pos_args)
        new_named = match.new_named_args(cur_named)
        environ["wsgiorg.routing_args"] = (new_pos, new_named)
        environ["webdispatch.urlmapper"] = self.urlmapper
        urlgenerator = URLGenerator(environ, self.urlmapper)
        environ["webdispatch.urlgenerator"] = urlgenerator
        environ["SCRIPT_NAME"] = script_name + splited[0]
        environ["PATH_INFO"] = extra_path_info

        return match.name

    def on_view_not_found(
        self,
        environ: Dict[str, Any],
        start_response: Callable[[str, List[Tuple[str, str]]], None],
    ) -> Iterable[bytes]:
        """ called when views not found"""
        start_response("404 Not Found", [("Content-type", "text/plain")])
        return [b"Not found"]
