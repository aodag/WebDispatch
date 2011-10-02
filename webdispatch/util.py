try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

def application_url(environ):
    """
    >>> env = {'wsgi.url_scheme': 'https',
    ...  'HTTP_HOST': 'example.com',
    ...  'SCRIPT_NAME': '/a',
    ...  'PATH_INFO': '/b'}
    >>> application_url(env)
    'https://example.com/a/b'
    """

    scheme = environ['wsgi.url_scheme']
    host = environ.get('HTTP_HOST')
    if not host:
        server_name = environ['SERVER_NAME']
        port = environ['SERVER_PORT']
        if scheme == 'https':
            if port == '433':
                host = server_name
            else:
                host = server_name + ":" + port
        else:
            if port == '80':
                host = server_name
            else:
                hsot = server_name + ":" + port
    script_name = quote(environ.get('SCRIPT_NAME', ''))
    path_info = quote(environ.get('PATH_INFO', ''))
    query_string = environ.get('QUERY_STRING')
    # return scheme + "://" + host + script_name + path_info + ('?' + query_string) if query_string else ''
    return urlunparse((scheme, host, script_name + path_info, '', query_string, ''))
