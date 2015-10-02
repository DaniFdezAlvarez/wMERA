__author__ = 'Dani'

from apps.mera_experiment.result_node import ExperimentResultNode


FILE_ORIGIN = 0
NUMBER_OF_LINE = 1
NUMBER_OF_ARTISTS = 2
ORIGINAL_QUERY = 3
SONG = 4
ARTIST_BEGIN = 5
ARTIST_END = -4
DISCOGS_ID = -1
COMMENT = -2
FOND_OR_NOT_FOUND = -3


class AolQueryGen(object):

    def __init__(self, matcher, aol_path_file):
        self._matcher = matcher
        self._aol_path_file = aol_path_file


    def run_queries(self):
        """
        Generator yielding objects of type ExperimentResultNode for each executed query
        :return:
        """
        with open(self._aol_path_file, "r") as file_io:
            file_io.readline()  # Ignoring heading
            for line in file_io:
                line = line.replace("\n", "")
                yield self._generate_result_node_from_raw_line(line)


    def _generate_result_node_from_raw_line(self, line):
        pieces = line.split("\t")
        target_id = pieces[DISCOGS_ID]
        song = pieces[SONG]
        writers = []
        artists = pieces[ARTIST_BEGIN:ARTIST_END + 1]
        list_of_results = self._matcher.find_song(name=song,
                                                  artists=artists + writers)
        return ExperimentResultNode(list_of_mera_base_results=list_of_results,
                                    target_id=target_id,
                                    song=song,
                                    artists=artists,
                                    writers=writers)


