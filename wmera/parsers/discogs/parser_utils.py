__author__ = 'Dani'

from wmera.mera_core.str_ops.normalization import normalize, remove_brackets_with_numbers
from wmera.mera_core.model.entities import ROLE_WRITER, ROLE_FEATURER
EMPTY_CONTENT = [None, ""]

WRITER_ROLES = ["Written-By", "Music By", "Producer"]
ARTIST_ROLES = ["Vocals", "Feat.", "Featuring"]


def get_subnodes_text(node):
    for elem in list(node):
        if elem.text not in [None, ""]:
            yield normalize_discogs_name(elem.text)


def normalize_discogs_name(original_text):
    """
    Many discogs name appear with a number between brackets. Im not sure
    about its meaning, but pretty sure about i should ignore them.
    We are erasing them here from the original strings.

    :param original_text:
    :return:
    """
    if original_text in EMPTY_CONTENT:
        return original_text
    return normalize(remove_brackets_with_numbers(original_text))


def map_discogs_role(role):
    for aWRole in WRITER_ROLES:
        if aWRole in role:
            return ROLE_WRITER
    for aARole in ARTIST_ROLES:
        if aARole in role:
            return ROLE_FEATURER