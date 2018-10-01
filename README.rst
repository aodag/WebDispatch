WebDispatch
============================

.. image:: https://travis-ci.org/aodag/WebDispatch.svg?branch=master
   :target: https://travis-ci.org/aodag/WebDispatch

.. image:: https://coveralls.io/repos/aodag/WebDispatch/badge.png?branch=master 
   :target: https://coveralls.io/r/aodag/WebDispatch?branch=master 

.. image:: https://img.shields.io/pypi/wheel/WebDispatch.svg
    :target: https://pypi.python.org/pypi/WebDispatch/
    :alt: Wheel Status

.. image:: https://codecov.io/gh/aodag/WebDispatch/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aodag/WebDispatch

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
  b'Hello, webdispatch'


Wildcard
+++++++++++++++

You can use wildcard after last slash.
Pattern with wildcard consumes paths before the wildcard, (and make that new script_name,)
and remained paths becomes new path_info.

::

  >>> @wsgify
  ... def with_pathinfo(request):
  ...     return "Hello, %s" % request.path_info
  >>> dispatcher.add_url('top', '/with_pathinfo/*', with_pathinfo)
  >>> req = Request.blank('/with_pathinfo/this/is/pathinfo')
  >>> res = req.get_response(dispatcher)
  >>> res.body
  b'Hello, this/is/pathinfo'

Type Converter
++++++++++++++++++

You can specify converter with varname below ":".

::

  >>> @wsgify
  ... def add(request):
  ...     result = request.urlvars['v1'] + request.urlvars['v2']
  ...     return "result, %d" % result
  >>> dispatcher.add_url('add', '/add/{v1:int}/{v2:int}', add)
  >>> req = Request.blank('/add/1/2')
  >>> res = req.get_response(dispatcher)
  >>> res.body
  b'result, 3'

default converters are defined as bellow::

   DEFAULT_CONVERTERS = {
       'int': int,
       'date': lambda s: datetime.strptime(s, '%Y-%m-%d'),
       'date_ym': lambda s: datetime.strptime(s, '%Y-%m'),
   }


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
  b'Hello'

Method Dispatch
-------------------------------------

dispatch by HTTP METHOD restfully.

use ``register_app`` decorator::

  >>> from webdispatch import MethodDispatcher
  >>> restapp = MethodDispatcher()
  >>> @restapp.register('get')
  ... @wsgify
  ... def get_hello(request):
  ...    return "Get Hello"
  >>> @restapp.register('post')
  ... @wsgify
  ... def post_hello(request):
  ...    return "Post Hello"



or use ``registe_app`` method::

  >>> from webdispatch import MethodDispatcher
  >>> restapp = MethodDispatcher()
  >>> restapp.register_app('get', get_hello)
  >>> restapp.register_app('post', post_hello)

Each applications are registered with HTTP Method name.

invoke WSGI application::

  >>> req = Request.blank('/')
  >>> res = req.get_response(restapp)
  >>> res.body
  b'Get Hello'

extra_environ
---------------------------

``DispatchBase`` accepts ``extra_environ`` argument.
Dispatcher adds that argument to wsgi environ by request.
