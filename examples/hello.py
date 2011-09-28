from webob.dec import wsgify
from webdispatch import Dispatcher

app = Dispatcher()

@wsgify
def index(request):
    url = request.environ['webdispatch.urlmapper'].generate("hello")
    return '<a href="%s">Hello</a>' % (url,)

@wsgify
def hello(request):
    return "Hello"

app.urlmapper.add('home', '/', index)
app.urlmapper.add('hello', '/hello', hello)

from wsgiref.simple_server import make_server

httpd = make_server('', 8080, app)
httpd.serve_forever()
