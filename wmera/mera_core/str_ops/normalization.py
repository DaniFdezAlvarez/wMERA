# coding=utf-8
__author__ = 'Dani'

import re
import unicodedata

_WHITE_SPACES = re.compile("[ \t\n\r]+")
_BRACKETS_WITH_NUMBERS = re.compile("\([0-9]*\)")
_BRACKETS_WITH_INFO = re.compile("\(.*\)")
_FORBIDDEN_PUNCTUATION = re.compile("[\.\"<>\{\}\|\\\^`´]")
_DOLLAR = re.compile("\$")

_EMPTY_CONTENT = [None, ""]


def normalize(original_str):
    if original_str in _EMPTY_CONTENT:
        return original_str
    result = original_str.lower()  # minus
    result = replace_forbidden_punctuation(result)
    result = replace_dollar(result)  # char '$' can be conflictive.
    result = replace_non_ascii(result)  # Non-ascii characters translated to similar ones
    result = re.sub(_WHITE_SPACES, " ", result)  # Useless white spaces
    result = result.strip()  # useless final spaces

    return result


def replace_dollar(original_str):
    return re.sub(_DOLLAR, "S", original_str)


def replace_forbidden_punctuation(original_str):
    return re.sub(_FORBIDDEN_PUNCTUATION, " ", original_str)


def replace_non_ascii(original_str):
    if type(original_str) == str:
        return unicodedata.normalize('NFKD', unicode(original_str, "utf-8")).encode('ascii', 'ignore')
    else:  # unicode
        return unicodedata.normalize('NFKD', original_str).encode('ascii', 'ignore')


def remove_brackets_with_numbers(original_str):
    return re.sub(_BRACKETS_WITH_NUMBERS, "", original_str)


def remove_brackets_info(original_str):
    return re.sub(_BRACKETS_WITH_INFO, "", original_str)

