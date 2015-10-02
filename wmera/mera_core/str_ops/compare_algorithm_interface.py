__author__ = 'Dani'


class CompareAlgoritmhInterface(object):

    @staticmethod
    def compare(str1, str2):
        """
        It receives 2 strings and return the degree of similarity between them according to
        some heuristic. The result must be a float number inn [0,1], where 1 means maximun
        similarity and 0 means minimum similarity
        :param str1:
        :param str2:
        :return:
        """
        raise NotImplementedError("")

