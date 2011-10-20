Tips and Tricks
=============================

integrate with WebOb
------------------------------------

WebOb has wsgify decorator that makes callable wsgi application.

WebDispatch provides :class:`webdispatch.mixins.URLMapperMixin` to add generate_url method to Request class.

use generator mixin::

  class MyRequest(Request, URLMapperMixin):
      pass

  @wsgify(RequestClass=MyRequest)
  def view(request):
      return "Hello"

generate absolute url on backend of reverse proxy.
-----------------------------------------------------------------

When application is forwarded by reverse proxy, below headers are given.

- HTTP_X_FORWARDED_SERVE
- HTTP_X_FORWARDED_HOST
- HTTP_X_FORWARDED_FOR
- HTTP_X_FORWARDED_SCHEME
- HTTP_X_FORWARDED_PROTO

use paste.deploy.config.PrefixMiddleware.

::

 [pipeline:main]
 pipeline =
    prefix
    app

 [filter:prefix]
 use = egg:PasteDeploy#prefix
 scheme = https



