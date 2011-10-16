from webdispatch import URLDispatcher
from webob.dec import wsgify

@wsgify
def handler(request):
    return request.url

@wsgify
def gen_handler(request):
    return request.environ['webdispatch.urlgenerator'].generate('sub_hello')

app = URLDispatcher()
app.add_url('top', '/', handler)
app.add_url('generating', '/gen', gen_handler)
app.add_url('sub_prefix', '/sub', handler)
sub_app = app.add_subroute('/sub/')
sub_app.add_url('sub_hello', 'x', handler)
sub_app.add_url('sub_gen', 'gen', gen_handler)
