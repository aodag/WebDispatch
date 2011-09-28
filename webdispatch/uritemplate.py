import re
import string
vars_pt = re.compile(r"{(?P<varname>[a-zA-Z0-9_]+)}")

def regex_replacer(m):
    d = m.groupdict()
    return "(?P<" + d['varname'] + r">\w+)"

def template_replacer(m):
    return "${" + m.groupdict()['varname'] + "}"

def pattern_to_regex(pattern):
    if len(pattern) > 0 and pattern[-1] == "*":
        pattern = pattern[:-1]
        end = ""
    else:
        end = "$"
    return "^" + vars_pt.sub(regex_replacer, pattern) + end

def pattern_to_template(pattern):
    return vars_pt.sub(template_replacer, pattern)

class URIMatch(object):
    def __init__(self, matchdict, matchlength):
        self.matchdict = matchdict
        self.matchlength = matchlength

class URITemplate(object):
    def __init__(self, tmpl_pattern):
        self.pattern = tmpl_pattern
        self.regex = re.compile(pattern_to_regex(tmpl_pattern))
        self.template = string.Template(pattern_to_template(tmpl_pattern))

    def match(self, path_info):
        m = self.regex.match(path_info)
        if m is None:
            return m
        matchlength = len(m.group(0))
        matchdict = m.groupdict()
        return URIMatch(matchdict, matchlength)

    def substitute(self, vars):
        return self.template.substitute(vars)
