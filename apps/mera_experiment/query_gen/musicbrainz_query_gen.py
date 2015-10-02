__author__ = 'Dani'

from apps.mera_experiment.result_node import ExperimentResultNode


DISCOGS_FILE_INDEX = 0
DISCOGS_ID = 1
NUMBER_OF_ARTIST = 2
SONG = 3
ARTISTS = 4
WRITERS = 5


class MusicbrainzQueryGen(object):
    def __init__(self, matcher, musicbrainz_path_file):
        self._matcher = matcher
        self._musicbrainz_path_file = musicbrainz_path_file


    def run_queries(self):
        """
        Generator yielding objects of type ExperimentResultNode for each executed query
        :return:
        """
        with open(self._musicbrainz_path_file, "r") as file_io:
            file_io.readline()  # Ignoring heading
            for line in file_io:
                line = line.replace("\n", "")
                yield self._generate_result_node_from_raw_line(line)


    def _generate_result_node_from_raw_line(self, line):
        pieces = line.split("\t")
        target_id = pieces[DISCOGS_ID]
        song = pieces[SONG]
        artists = [artist for artist in pieces[ARTISTS].split("|")] if pieces[ARTISTS] != "-" else []
        writers = [writer for writer in pieces[WRITERS].split("|")] if pieces[WRITERS] != "-" else []
        list_of_results = self._matcher.find_song(name=song,
                                                  artists=artists + writers)
        return ExperimentResultNode(list_of_mera_base_results=list_of_results,
                                    target_id=target_id,
                                    song=song,
                                    artists=artists,
                                    writers=writers)



