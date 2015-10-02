__author__ = 'Dani'
from random import randint



class BmatExtractor(object):

    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._num_lines = self._read_number_of_lines()


    def _read_number_of_lines(self):
        counter = 0
        with open(self._path_to_file, "r") as bmat_file:
            for line in bmat_file:
                counter += 1
        return counter


    def _get_random_index(self, num_lines):
        result = set()
        while len(result) != num_lines:
            result.add(randint(1, self._num_lines))  # First line should be ignored
        result = list(result)
        result.sort()
        return result


    def get_random_artist_names(self, num_artist=100):
        result = []
        for line in self.get_random_complete_lines(num_artist):
            one_or_more_artist = line.split("\t")[1].split("||")
            result.append(one_or_more_artist[randint(0, len(one_or_more_artist) - 1)].strip())
        return result

    def get_random_complete_lines(self, num_lines=100):
        result = []
        counter_line = 0
        counter_success = 0
        indexes = self._get_random_index(num_lines * 2)
        with open(self._path_to_file, "r") as bmat_file:
            for line in bmat_file:
                if counter_line in indexes and self._is_complete_line(line):
                    result.append(line.replace("\n", ""))
                    counter_success += 1
                    if counter_success >= num_lines:
                        break
                counter_line += 1
        return result

    def _is_complete_line(self, line):
        parts = line.split("\t")
        if len(parts) != 7 or parts[1] == "":
            return False
        return True
