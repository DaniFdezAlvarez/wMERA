__author__ = 'Dani'


SEPARATOR = "|"


def list_to_tsv_field(list_att):
    if len(list_att) == 0:
        return ""
    result = list_att[0]
    for i in range(1, len(list_att)):
        result += SEPARATOR + list_att[i]
    return result