def hello(environ, start_response):
    start_response("200 OK",
        [('Content-type', 'text/plain')])
    return ["hello"]

def goodbye(environ, start_response):
    start_response("200 OK",
        [('Content-type', 'text/plain')])
    return ["goodby %s" % environ['wsgiorg.routing_args'][1]['name']]

from webdispatch import URLDispatcher
application = URLDispatcher()
application.add_url('hello', '/hello', hello)
application.add_url('goodbye', '/good-bye', goodbye)

from wsgiref.simple_server import make_server

httpd = make_server('0.0.0.0', 8080, application)
httpd.serve_forever()
