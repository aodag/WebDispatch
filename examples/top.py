from webdispatch import URLDispatcher
from webob.dec import wsgify

@wsgify
def top(request):
    return request.environ['webdispatch.urlgenerator'].generate('top')

app = URLDispatcher()
app.add_url('top', '/', top)

