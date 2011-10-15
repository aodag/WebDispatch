try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

def application_url(environ, path):
    """
    >>> env = {'wsgi.url_scheme': 'https',
    ...  'HTTP_HOST': 'example.com',
    ...  'SCRIPT_NAME': '/a',
    ...  'PATH_INFO': '/b'}
    >>> application_url(env, '/c')
    'https://example.com/a/c'
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
    query_string = environ.get('QUERY_STRING')
    return urlunparse((scheme, host, script_name + path, '', query_string, ''))
