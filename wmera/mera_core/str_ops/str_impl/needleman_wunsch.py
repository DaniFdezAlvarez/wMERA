__author__ = 'Dani'


from wmera.mera_core.str_ops.compare_algorithm_interface import CompareAlgoritmhInterface


_NO_POINTER = -2
_TOP = 1
_LEFT = -1
_DIAGONAL = 0

_MATCHING = 1
_GAP = '-'


class NeedlemanWunsch(CompareAlgoritmhInterface):



    @staticmethod
    def compare(str1, str2):
        """
        We will use a version of the algorithm in which every symbol has a similarity of _MATCHING with itself
        and a penalization of - _MATCHING with the rest of symbols. No matrix of similarities for alphabet will
         be defined.

        """
        #### type checking
        if str1 is None or str2 is None or not (type("") == type(str1) == type(str2)):
            raise ValueError("Params should be strings")

        if len(str1) == 0 or len(str2) == 0:
            return 0.0

        short_str, long_str = (str1.upper(), str2.upper()) if len(str1) >= len(str2) else (str2.upper(), str1.upper())

        #### Phase 1 -- Initializing matrix
        matrix = []
        for i in range(0, len(short_str) + 1):
            a_row = []
            matrix.append(a_row)
            for j in range(0, len(str2) + 1):
                a_row.append(NWCell())

        for i in range(1, len(short_str) + 1):
            matrix[i][0].score = -i
            matrix[i][0].pointer = _TOP

        for j in range(1, len(long_str) + 1):
            matrix[0][j].score = -j
            matrix[0][j].pointer = _LEFT

        #### Phase 2 -- Deducing cell values:
        for i in range(1, len(short_str) + 1):
            for j in range(1, len(long_str) + 1):
                coincidence = -_MATCHING if short_str[i - 1] != long_str[j - 1] else _MATCHING
                if matrix[i - 1][j - 1].score >= matrix[i - 1][j].score:
                    if matrix[i - 1][j - 1].score >= matrix[i][j - 1].score:
                        matrix[i][j].score = matrix[i - 1][j - 1].score + coincidence
                        matrix[i][j].pointer = _DIAGONAL
                    else:
                        matrix[i][j].score = matrix[i][j - 1].score + coincidence
                        matrix[i][j].pointer = _LEFT
                else:
                    if matrix[i - 1][j].score >= matrix[i][j - 1].score:
                        matrix[i][j].score = matrix[i - 1][j].score + coincidence
                        matrix[i][j].pointer = _TOP
                    else:
                        matrix[i][j].score = matrix[i][j - 1].score + coincidence
                        matrix[i][j].pointer = _LEFT
        # for i in range(0, len(short_str) + 1):
        #     row = ""
        #     for j in range(0, len(long_str) + 1):
        #         row += str(matrix[i][j].pointer) + "\t"
        #     print row

        #### Phase 3 -- Collecting results
        short_alignment, long_alignment = "", ""

        i, j = len(short_str), len(long_str)
        while not (i == 0 and j == 0):
            if matrix[i][j].pointer == _DIAGONAL:
                short_alignment += short_str[i - 1]
                long_alignment += long_str[j - 1]
                i -= 1
                j -= 1
            elif matrix[i][j].pointer == _LEFT:
                short_alignment += _GAP
                long_alignment += long_str[j - 1]
                j -= 1
            else:  # _TOP
                short_alignment += short_str[i - 1]
                long_alignment += _GAP
                i -= 1

        short_alignment, long_alignment = short_alignment[::-1], long_alignment[::-1]

        #### Phase 4. Interpreting results
        parts, coincidences = NeedlemanWunsch._interpret_alignment(short_alignment, long_alignment)

        # 1st criteria. The max score (1) is reached when there as many aligned chars as
        # the number of chars in the longest chain. We will subtract of that result
        # the amount of 1/len(long_alignement) for every non-aligned character,
        # including gaps

        result = 1.0 - (float(len(long_str) - coincidences) / len(long_str))

        # 2nd criteria.
        # The number of parts will be penalized. We consider better a than b,
        # and d much better than d where:
        # a)
        # shakira
        # shakir_
        # b)
        # shakira
        # sha_ira
        #
        # c)
        # shakirashakira
        # shakira-------
        # d)
        # shakirashakira
        # s-a-i-a-h-k-r-
        #
        # Both pairs of alignement have the same num of coincidences and the same
        # lenght, but b and d has a more splited short chain to make the
        # alignment. It looks like 'shakirashakira' has not much to do with 'saiahkr'
        # and that should be reflected.
        #
        # len(short_target) == max possible splitted parts

        result *= (len(short_str) + 1 - parts) / float(len(short_str))

        return result

    @staticmethod
    def _interpret_alignment(alignment_original_short, alignment_original_long):
        """

        It returns the number of aligned chars and the number of parts in which the short string
        has been splitted in order to reach the best alignement.

        The string params are expected to have the same length.
        Short_str could contain _GAP characters or not. long should not contain it.

        """
        # print alignment_original_short, alignment_original_long
        parts = 1
        coincidences = 0
        last_char_was_a_gap = True
        i = 0
        ### looking for firts non-gap
        while i < len(alignment_original_short):
            if alignment_original_short[i] != _GAP:
                break
            i += 1
        ### calculating parts and coincidences
        while i < len(alignment_original_short):  # One of the chains. not mattering which one.They have the same length
            if alignment_original_short[i] == _GAP:
                if not last_char_was_a_gap:
                    last_char_was_a_gap = True
                    parts += 1
            else:
                if alignment_original_short[i] == alignment_original_long[i]:
                    coincidences += 1
                if last_char_was_a_gap:
                    last_char_was_a_gap = False
            i += 1
        if alignment_original_short[-1] == _GAP:
            parts -= 1
        return parts, coincidences


class NWCell(object):
    """
    This represents a cell of a matrix in the NW algorithm. It stores information of score and pointing direction

    """

    def __init__(self, score=0, pointer=_NO_POINTER):
        self.score = score
        self.pointer = pointer