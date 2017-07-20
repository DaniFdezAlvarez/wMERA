from apps.discogs_survey_experiment.consts import _CHAR_MISSED,_CHAR_LOW, _CHAR_NA

def array_str_ints(first, last):
    result = []
    for i in range(first, last + 1):
        result.append(str(i))
    return result


def aceptable_position_chars(first=1, last=20):
    return [_CHAR_MISSED, _CHAR_LOW, _CHAR_NA] + array_str_ints(first, last)


def is_better_pos(reference, new):
    """
    COnsideraremos N/A como mejor que missed. No es algo que importe realmente
    :param reference:
    :param new:
    :return:
    """
    if reference == _CHAR_NA:
        if new == _CHAR_NA:
            return False
        return True

    elif reference == _CHAR_MISSED:
        if new in [_CHAR_MISSED, _CHAR_NA]:
            return False
        return True

    elif reference == _CHAR_LOW:
        if new in [_CHAR_MISSED, _CHAR_NA, _CHAR_LOW]:
            return False
        return True

    elif new in [_CHAR_MISSED, _CHAR_NA, _CHAR_LOW]:  # At this point, reference should be a number
        return False

    else:  # At this point, both should be numbers
        return True if int(new) < int(reference) else False