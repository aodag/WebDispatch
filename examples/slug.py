from webdispatch.urldispatcher import URLDispatcher
from webob.dec import wsgify


@wsgify
def slug(request):
    slug = request.urlvars['slug']
    return slug


app = URLDispatcher()
app.add_url('slug', '/{slug}', slug)
