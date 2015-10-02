__author__ = 'Dani'




class StringComparator(object):

    def __init__(self, list_of_classes_of_algorithms):
        if not isinstance(list_of_classes_of_algorithms, list):
            raise ValueError("Expecting a list of comparation algoritms")
        if len(list_of_classes_of_algorithms) == 0:
            raise ValueError("At leats an algorithm needed")
        self._algorithms = list_of_classes_of_algorithms


    def compare_str(self, str1, str2):
        results = []
        for an_algoritmh in self._algorithms:
            results.append(an_algoritmh.compare(str1, str2))
        return max(results)


