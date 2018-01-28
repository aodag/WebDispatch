from webdispatch.urldispatcher import URLDispatcher
from webob import Request
from webob.dec import wsgify
from webdispatch.mixins import URLMapperMixin


class MyRequest(Request, URLMapperMixin):
    pass


class WebObDispatcher(URLDispatcher):
    def add_url(self, name, pattern, view):
        application = wsgify(view, RequestClass=MyRequest)
        super(WebObDispatcher, self).add_url(name, pattern, application)


def index(request: MyRequest) -> str:
    url = request.generate_url("hello", xname="webdispatch")
    return '<a href="%s">Hello</a>' % (url,)


def hello(request: MyRequest) -> str:
    return "Hello %s" % request.urlvars['xname']


app = WebObDispatcher()
app.add_url('home', '/', index)
app.add_url('hello', '/hello/{xname}', hello)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('0.0.0.0', 8080, app)
    httpd.serve_forever()
