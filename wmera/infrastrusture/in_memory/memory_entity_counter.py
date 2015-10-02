__author__ = 'Dani'

import json

from wmera.mera_core.mera_infrastructure.entity_counter_interface import EntityCounterInterface, ARTIST_TYPE, SONG_TYPE


class MemoryEntityCounter(EntityCounterInterface):

    def __init__(self, load_file=None):
        self._counter_dict = {ARTIST_TYPE: 0,
                              SONG_TYPE: 0}
        if load_file is not None:
            self.load_content(load_file)


    def reset_count(self, types=None):
        """
        If types is None, it will reset all the counts.
        Else, it expects types to be a list of string containing types
        of entity counts to reset.

        :param types:
        :return:
        """
        self._counter_dict[ARTIST_TYPE] = 0
        self._counter_dict[SONG_TYPE] = 0

    def increase_artists(self, num_artists=1):
        """
        Increse in num_artists units the stored number of artist present in the graph.
        :param num_artists:
        :return:
        """
        self._counter_dict[ARTIST_TYPE] += num_artists


    def number_of_artists(self):
        """
        It returns the total number of artist stored in the system.
        :return:
        """
        return self._counter_dict[ARTIST_TYPE]


    def increase_songs(self, num_songs=1):
        """
        Increase in num_songs units the stored number of songs present in the graph.

        :param num_songs:
        :return:
        """
        self._counter_dict[SONG_TYPE] += num_songs


    def number_of_songs(self):
        """
        It returns the total number of songs stored in the system.

        :return:
        """
        return self._counter_dict[SONG_TYPE]


################# Special public methods

    def save_content(self, file_path):
        with open(file_path, "w") as file_content:
            json.dump(self._counter_dict, file_content)


    def load_content(self, file_path):
        with open(file_path, "r") as file_content:
            self._counter_dict = json.load(file_content)


