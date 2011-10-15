Tips and Tricks
=============================

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



