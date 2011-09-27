from .uritemplate import URITemplate

class RegexDispatch(object):

    def __init__(self, applications):
        self.patterns = []
        for pattern, application in applications:
            self.add_application(pattern, application)

    def add_application(self, pattern, application):
        self.patterns.append((URITemplate(pattern), application))

    def __call__(self, environ, start_response):
        script_name = environ.get('SCRIPT_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        for regex, application in self.patterns:
            match = regex.match(path_info)
            if match is None:
                continue
            extra_path_info = path_info[match.matchlength:]
            if extra_path_info and not extra_path_info.startswith('/'):
                # Not a very good match
                continue
            #pos_args = match.groups()
            pos_args = []
            named_args = match.matchdict
            cur_pos, cur_named = environ.get('wsgiorg.routing_args', ((), {}))
            new_pos = list(cur_pos) + list(pos_args)
            new_named = cur_named.copy()
            new_named.update(named_args)
            environ['wsgiorg.routing_args'] = (new_pos, new_named)
            environ['SCRIPT_NAME'] = script_name + path_info[:match.matchlength]
            environ['PATH_INFO'] = extra_path_info
            return application(environ, start_response)
        return self.not_found(environ, start_response)

    def not_found(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return ['Not found']
