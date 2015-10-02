__author__ = 'Dani'

from wmera.mera_core.str_ops.normalization import normalize




def extract_unique_ngrams(original_str, size=3):
    """
    Function to extract n-grams, 3-grams actually. It returns a list
    of the n-grams of $size size in original_str.
    If an n-gram appears twice (or more times) it will appear
    only once in the final list.

    :param original_str:
    :param size:
    :return:
    """
    if len(original_str) < size:
        return [original_str.lower()]
    original_str = original_str.lower()
    dict_result = set()
    for i in range(0, len(original_str) - size + 1):
        dict_result.add(original_str[i:i + size])
    return list(dict_result)


def extract_unique_normalized_ngrmas(original_str, size=3):
    """
    Function to extract n-grams, 3-grams actually. It returns a list
    of the n-grams of $size size in the resulting str of normalizing
    original_str.
    If an n-gram appears twice (or more times) it will appear
    only once in the final list.

    :param original_str:
    :param size:
    :return:
    """
    return extract_unique_ngrams(normalize(original_str), size)
