import re

vars_pt = re.compile(r"{([^}]+)}")

def replacer(m):
    return "(?P<" + m.group(1) + r">\w+)"

def pattern_to_regex(pattern):
    return "^" + vars_pt.sub(replacer, pattern) + "$"

class URITemplate(object):
    def __init__(self, tmpl_pattern):
        self.pattern = tmpl_pattern
        self.regex = re.compile(pattern_to_regex(tmpl_pattern))

    def match(self, path_info):
        m = self.regex.match(path_info)
        if m is None:
            return m

        return m.groupdict()
