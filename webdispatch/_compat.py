try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse
