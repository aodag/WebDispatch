WebDispatch
================================

``WebDispatch`` is dispatcher collection for wsgi application.
That has no dependency to exsiting frameworks, but works fine with WebOb.

.. _url-dispatcher:

Dispatch and Generate URL
------------------------------------

dispatch with url patterns.

>>> dispatcher = URLDispatcher()
>>> dispatcher.add_url('top', url, wsgiref.simple_server.demoapp)
