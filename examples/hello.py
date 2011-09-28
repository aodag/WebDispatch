from webob import Request
from webob.dec import wsgify
from webdispatch import Dispatcher
from webdispatch.mixins import URLMapperMixin

class MyRequest(Request, URLMapperMixin):
    pass

app = Dispatcher()

@wsgify(RequestClass=MyRequest)
def index(request):
    url = request.generate_url("hello")
    return '<a href="%s">Hello</a>' % (url,)

@wsgify(RequestClass=MyRequest)
def hello(request):
    return "Hello"

app.add_url('home', '/', index)
app.add_url('hello', '/hello', hello)

from wsgiref.simple_server import make_server

httpd = make_server('', 8080, app)
httpd.serve_forever()
