""" uri template
parsing and generating url patterns
"""

from datetime import datetime
import re
import string
from typing import (  # noqa pylint: disable=unused-import
    Any,
    Dict,
    Callable,
    Tuple,
)
from mypy_extensions import TypedDict

VARS_PT = re.compile(r"{(?P<varname>[a-zA-Z0-9_]+)"
                     r"(:(?P<converter>[a-zA-Z0-9_]+))?}",
                     re.X)
META_CHARS = (
    "\\",
    ".",
    "^",
    "$",
    "*",
    "+",
    "|",
    "?",
    "(",
    ")",
    "[",
    "]")  # type: Tuple[str, ...]

DEFAULT_CONVERTERS = {
    'int': int,
    'date': lambda s: datetime.strptime(s, '%Y-%m-%d'),
    'date_ym': lambda s: datetime.strptime(s, '%Y-%m'),
}  # type: Dict[str, Callable]


def regex_replacer(matched) -> str:
    """ replace url placeholder to regex pattern"""
    values = matched.groupdict()
    return "(?P<" + values['varname'] + r">[\w-]+)"


def template_replacer(matched) -> str:
    """ replace url placeholder to template interpolation"""
    values = matched.groupdict()
    return "${" + values['varname'] + "}"


def pattern_to_regex(pattern: str) -> str:
    """ convert url patten to regex """
    if pattern and pattern[-1] == "*":
        pattern = pattern[:-1]
        end = ""
    else:
        end = "$"
    for metac in META_CHARS:
        pattern = pattern.replace(metac, "\\" + metac)

    return "^" + VARS_PT.sub(regex_replacer, pattern) + end


def pattern_to_template(pattern: str) -> str:
    """ convert url pattern to string template"""
    return VARS_PT.sub(template_replacer, pattern)


def detect_converters(pattern: str,
                      converter_dict: Dict[str, Callable],
                      default: Callable = str):
    """ detect pairs of varname and converter from pattern"""
    converters = {}
    for matched in VARS_PT.finditer(pattern):
        matchdict = matched.groupdict()
        varname = matchdict['varname']
        converter = matchdict['converter']
        converters[varname] = converter_dict.get(converter, default)
    return converters


class URITemplateFormatException(Exception):
    """ raised when uri template format error duaring"""


MATCH_RESULT_TYPE = TypedDict(
    "MATCH_RESULT_TYPE",
    {"matchdict": Dict[str, Any], "matchlength": int})


class URITemplate(object):
    """ parsing and generating url with patterned """

    def __init__(self, tmpl_pattern: str,
                 converters=None) -> None:
        if tmpl_pattern.endswith('*') and not tmpl_pattern.endswith('/*'):
            raise URITemplateFormatException('wildcard must be after slash.')

        self.pattern = tmpl_pattern
        self.regex = re.compile(pattern_to_regex(tmpl_pattern))
        self.template = string.Template(pattern_to_template(tmpl_pattern))
        if converters is None:
            converters = DEFAULT_CONVERTERS
        self.converters = detect_converters(
            tmpl_pattern, converters)

    def match(self, path_info: str) -> MATCH_RESULT_TYPE:
        """ parse path_info and detect urlvars of url pattern """
        matched = self.regex.match(path_info)
        if matched is None:
            return None
        matchlength = len(matched.group(0))
        matchdict = matched.groupdict()

        try:
            matchdict = self.convert_values(matchdict)
        except ValueError:
            return None

        return {"matchdict": matchdict,
                "matchlength": matchlength}

    def convert_values(self, matchdict: Dict[str, str]) -> Dict[str, Any]:
        """ convert values of ``matchdict``
        with converter this object has."""

        converted = {}
        for varname, value in matchdict.items():
            converter = self.converters[varname]
            converted[varname] = converter(value)
        return converted

    def substitute(self, values: Dict[str, Any]) -> str:
        """ generate url with url template"""
        return self.template.substitute(values)
