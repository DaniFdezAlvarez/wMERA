__author__ = 'Dani'

from wmera.mera_core.str_ops.compare_algorithm_interface import CompareAlgoritmhInterface


_NO_POINTER = -2
_TOP = 1
_LEFT = -1
_DIAGONAL = 0

_MATCHING = 1
_GAP = '-'


class SmithWaterman(CompareAlgoritmhInterface):

    @staticmethod
    def compare(str1, str2):
        """
        We will use a version of the algotimh in wich every symbol has a similiratity of _MATCHING with itself
        and a penalization of - _MATCHING with the rest of symbols. No matrix of similarities for alphabeth will
         be defined.

        """
        # ### type checking
        if str1 is None or str2 is None or not (type("") == type(str1) == type(str2)):
            raise ValueError("Params should be strings")

        if len(str1) == 0 or len(str2) == 0:
            return 0.0

        short_str, long_str = (str1.upper(), str2.upper()) if len(str1) >= len(str2) else (str2.upper(), str1.upper())

        # ### Phase 1 -- Initializing matrix
        matrix = []
        for i in range(0, len(short_str) + 1):
            a_row = []
            matrix.append(a_row)
            for j in range(0, len(str2) + 1):
                a_row.append(SWCell())

        # ### Phase 2 -- Deducing cell values:
        max_score = 0
        max_i, max_j = 0, 0
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

                if 0 >= matrix[i][j].score:
                    matrix[i][j].score = 0
                    matrix[i][j].pointer = _NO_POINTER
                elif matrix[i][j].score > max_score:
                    max_score = matrix[i][j].score
                    max_i, max_j = i, j


        #### Phase 3 -- Collecting results
        short_alignment, long_alignment = "", ""

        i, j = max_i, max_j
        while not (matrix[i][j].score == 0):
            if matrix[i][j].pointer == _DIAGONAL:
                short_alignment += short_str[i - 1]
                long_alignment += long_str[j - 1]
                i -= 1
                j -= 1
            elif matrix[i][j].pointer == _LEFT:
                short_alignment += _GAP
                long_alignment += long_str[j - 1]
                j -= 1
            elif matrix[i][j].pointer == _TOP:
                short_alignment += short_str[i - 1]
                long_alignment += _GAP
                i -= 1
            else:  # NO POINTER
                raise BaseException("NO_POINTER? This can't be happening...")

        short_alignment, long_alignment = short_alignment[::-1], long_alignment[::-1]

        #### Phase 4. Interpreting results
        return float(len(short_alignment)) / float(len(long_str))


class SWCell(object):
    """
    This represents a cell of a matrix in the NW algorithm. It stores information of score and pointing direction

    """

    def __init__(self, score=0, pointer=_NO_POINTER):
        self.score = score
        self.pointer = pointer

