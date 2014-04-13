""" uri template
parsing and generating url patterns
"""

import re
import string

VARS_PT = re.compile(r"{(?P<varname>[a-zA-Z0-9_]+)}")
META_CHARS = ("\\", ".", "^", "$", "*", "+", "|", "?", "(", ")", "[", "]")


def regex_replacer(matched):
    """ replace url placeholder to regex pattern"""
    values = matched.groupdict()
    return "(?P<" + values['varname'] + r">[\w-]+)"


def template_replacer(matched):
    """ replace url placeholder to template interpolation"""
    values = matched.groupdict()
    return "${" + values['varname'] + "}"


def pattern_to_regex(pattern):
    """ convert url patten to regex """
    if len(pattern) > 0 and pattern[-1] == "*":
        pattern = pattern[:-1]
        end = ""
    else:
        end = "$"
    for metac in META_CHARS:
        pattern = pattern.replace(metac, "\\" + metac)

    return "^" + VARS_PT.sub(regex_replacer, pattern) + end


def pattern_to_template(pattern):
    """ convert url pattern to string template"""
    return VARS_PT.sub(template_replacer, pattern)


class URIMatch(object):
    """ represents matched results of uri template """
    def __init__(self, matchdict, matchlength):
        self.matchdict = matchdict
        self.matchlength = matchlength


class URITemplateFormatException(Exception):
    """ raised when uri template format error duaring"""


class URITemplate(object):
    """ parsing and generating url with patterned """
    def __init__(self, tmpl_pattern):
        if tmpl_pattern.endswith('*') and not tmpl_pattern.endswith('/*'):
            raise URITemplateFormatException('wildcard must be after slash.')

        self.pattern = tmpl_pattern
        self.regex = re.compile(pattern_to_regex(tmpl_pattern))
        self.template = string.Template(pattern_to_template(tmpl_pattern))

    def match(self, path_info):
        """ parse path_info and detect urlvars of url pattern """
        matched = self.regex.match(path_info)
        if matched is None:
            return matched
        matchlength = len(matched.group(0))
        matchdict = matched.groupdict()
        return URIMatch(matchdict, matchlength)

    def substitute(self, values):
        """ generate url with url template"""
        return self.template.substitute(values)
