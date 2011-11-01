WebDispatch
============================

WebDispatch is dispatcher collection for wsgi application. 
That has no dependency to exsiting frameworks, but works fine with `WebOb <http://www.webob.org>`_.

Dispatch and Generate URL
-----------------------------------------------

dispatch with url patterns.

example helo application::

  >>> from webob.dec import wsgify
  >>> @wsgify
  ... def greeting(request):
  ...     return "Hello, %s" % request.urlvars['name']

create and configure URL Dispatcher::

  >>> from webdispatch import URLDispatcher
  >>> dispatcher = URLDispatcher()
  >>> dispatcher.add_url('top', '/hello/{name}', greeting)

invoke dispatcher as WSGI Application::

  >>> from webob import Request
  >>> req = Request.blank('/hello/webdispatch')
  >>> res = req.get_response(dispatcher)
  >>> res.body
  'Hello, webdispatch'

Action Dispatch
-------------------------------------------------

ActionDispatcher invokes object method with action name from urlvars.

action handler class::

  >>> class MyHandler(object):
  ...     @wsgify
  ...     def greeting(self, request):
  ...         return "Hello"

create and configure ActionDispatcher::

  >>> from webdispatch import ActionDispatcher
  >>> actiondispatcher = ActionDispatcher()
  >>> actiondispatcher.register_actionhandler(MyHandler)

add action url with urlvars named action::

  >>> dispatcher.add_url('action_dispatch', '/actions/{action}', actiondispatcher)

invoke wsgi appclication.::

  >>> req = Request.blank('/actions/greeting')
  >>> res = req.get_response(dispatcher)
  >>> res.body
  'Hello'

Method Dispatch
-------------------------------------

dispatch by HTTP METHOD restfully.

sample wsgi app::

  >>> @wsgify
  ... def get_hello(request):
  ...    return "Get Hello"
  >>> @wsgify
  ... def post_hello(request):
  ...    return "Post Hello"

create and configure::

  >>> from webdispatch import MethodDispatcher
  >>> restapp = MethodDispatcher()
  >>> restapp.register_app('get', get_hello)
  >>> restapp.register_app('post', post_hello)

Each applications are registered with HTTP Method name.

invoke WSGI application::

  >>> req = Request.blank('/')
  >>> res = req.get_response(restapp)
  >>> res.body
  'Get Hello'
