""" dummy applications for testing paste.app_factory"""


def greeting(_, start_response):
    """ dummy application returns Hello simply"""
    start_response("200 OK", [("Content-type", "text/plain")])
    return [b"Hello"]


def bye(_, start_response):
    """ dummy application returns by simply"""
    start_response("200 OK", [("Content-type", "text/plain")])
    return [b"bye"]
