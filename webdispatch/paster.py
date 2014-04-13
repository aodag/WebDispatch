import sys
from .urldispatcher import URLDispatcher


def make_urldispatch_application(global_conf, **settings):
    patterns = [p.split("=", 1)
                for p in settings['patterns'].split('\n')
                if p]
    application = URLDispatcher()

    for pattern, app in patterns:
        pattern = pattern.strip()
        app = app.strip()
        mod, obj = app.split(":", 1)
        if mod not in sys.modules:
            __import__(mod)
        mod = sys.modules[mod]
        obj = getattr(mod, obj)
        application.add_url(app, pattern, obj)

    return application
