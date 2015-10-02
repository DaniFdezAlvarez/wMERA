__author__ = 'Dani'

from wmera.mera_core.str_ops.compare_algorithm_interface import CompareAlgoritmhInterface

_OP_COST = 2
_SWAP_COST = 1
_MULTIPLIER = 2


class WeightedDamerauLevenshtein(CompareAlgoritmhInterface):


    @staticmethod
    def compare(str1, str2):
        if str1 is None or str2 is None or not (type("") == type(str1) == type(str2)):
            raise ValueError("Params should be strings")

        if len(str1) == 0 or len(str2) == 0:  # if empty word
            return 0  # Max distance

        str_long = str_short = None

        if len(str1) >= len(str2):
            str_long = str1.upper()
            str_short = str2.upper()
        else:
            str_long = str2.upper()
            str_short = str1.upper()

        previous2_cost_array = []
        previous_cost_array = []
        cost_array = []

        char_str_long = None
        char_str_short = None

        left_multiplier = 1
        was_left_space = True
        top_multiplier = 1
        was_top_space = True

        for i in range(0, len(str_long) + 1):
            # Initializing r1 array, but only the first pos matters.
            # the rest of arrays are only manipulated to let them have
            # len(str1) +1  positions and access randomly to them later.
            cost_array.append(0)
            previous_cost_array.append(i * _OP_COST)
            previous2_cost_array.append(0)

        for j in range(1, len(str_short) + 1):
            char_str_short = str_short[j - 1]
            cost_array[0] = j * _OP_COST

            top_multiplier = _MULTIPLIER if was_top_space else 1
            was_top_space = char_str_short == ' '

            for i in range(1, len(str_long) + 1):
                char_str_long = str_long[i - 1]
                left_multiplier = _MULTIPLIER if was_left_space else 1
                was_left_space = char_str_long == ' '

                cost = 0 if char_str_long == char_str_short else _OP_COST

                # minimum of cell to the left+1, to the top+1, diagonally left
                # and up +cost
                cost_array[i] = min(cost_array[i - 1] + _OP_COST * left_multiplier,
                                    previous_cost_array[i] + _OP_COST * top_multiplier,
                                    previous_cost_array[i - 1] + cost * max(left_multiplier, top_multiplier))

                if i > 1 and j > 1 \
                        and str_long[i - 1] == str_short[j - 2] \
                        and str_long[i - 2] == str_short[j - 1]:
                    cost_array[i] = min(cost_array[i],
                                        previous2_cost_array[i - 2] + _SWAP_COST)
            #  copy current distance counts to 'previous row' distance counts
            aux_array = previous_cost_array
            previous_cost_array = cost_array
            cost_array = previous2_cost_array
            previous2_cost_array = aux_array

        # our last action in the above loop was to switch r0 and r1, so r1 now
        # actually has the most recent cost counts
        return 1.0 - (float(previous_cost_array[len(str_long)]) /
                      (_OP_COST * max(len(str_long), len(str_short)) + _OP_COST))
