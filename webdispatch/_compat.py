try:
    from urllib import quote
except ImportError: #pragma no cover
    from urllib.parse import quote
try:
    from urlparse import urlunparse
except ImportError: #pragma no cover
    from urllib.parse import urlunparse
