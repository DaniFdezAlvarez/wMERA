__author__ = 'Dani'



def extract_unique_ngrams(str1, size=3):
    """
    Function to extract n-grams, 3-grams actually. It returns a list
    of the n-grams of $size size in str1.
    If an n-gram appears twice (or more times) it will appear
    only once in the final list.

    :param str1:
    :param size:
    :return:
    """
    if len(str1) < size:
        return [str1]
    dict_result = set()
    for i in range(0, len(str1) - size + 1):
        dict_result.add(str1[i:i + size])
    return list(dict_result)


def extract_ngrams(word, size=3):
    if len(word) < size:
        return [word]
    result = []
    for i in range(0, len(word) - size + 1):
        result.append(word[i:i + size])
    return result


def compare_levenshtein(str1, str2):
    """

    :param str1: string param
    :param str2: string param
    :return: float number in the range [0,1]. 1 is the minimun distance, 0 is the max distance.
    """

    if str1 is None or str2 is None or not (type("") == type(str1) == type(str2)):
        print type(str1), type(str2)
        raise ValueError("Params should be strings")

    if len(str1) == 0 or len(str2) == 0:  # if empty word
        return 0  # Max distance

    str1_upper = str1.upper()
    str2_upper = str2.upper()

    previous_cost_array = []
    cost_array = []
    tmp_list = []  # placeholder to assist in swapping p and d

    char_1 = None
    char_2 = None

    cost = 0

    previous_cost_array += range(0, len(str1_upper) + 1)
    cost_array += range(0, len(str1_upper) + 1)  # This should be done to have an array of len(str1) positions.
                                                # Values does not matter at this point

    for j in range(1, len(str2_upper) + 1):
        char_2 = str2_upper[j - 1]
        cost_array[0] = j

        for i in range(1, len(str1_upper) + 1):
            char_1 = str1_upper[i - 1]
            if char_1 == char_2:
                cost = 0
            else:
                cost = 1
            cost_array[i] = min(cost_array[i - 1] + 1,
                                previous_cost_array[i] + 1,
                                previous_cost_array[i - 1] + cost)

        tmp_list = previous_cost_array
        previous_cost_array = cost_array
        cost_array = tmp_list

    return 1.0 - (float(previous_cost_array[len(str1)]) / max(len(str1), len(str2)))

