__author__ = 'Dani'

import unittest

from wmera.parsers.discogs.song_parser import DiscogsSongParser
from wmera.mera_core.model.entities import Dataset, ROLE_WRITER
from wmera.utils import rel_path_to_file


class TestDiscogsSongParser(unittest.TestCase):

    def test_entity_detection(self):
        parser = DiscogsSongParser(file_path=rel_path_to_file("../../files/releases_piece_big.xml", __file__),
                                   dataset=Dataset(title="TestDataset"))

        counter_songs = 0
        counter_writers = 0
        for a_song in parser.parse_songs():
            counter_songs += 1
            for a_coll in a_song.collaborations:
                if a_coll.role == ROLE_WRITER:
                    counter_writers += 1
            for an_alt in a_song.alternative_titles:
                print a_song.canonical, an_alt

        self.assertEqual(281, counter_songs, msg="Expected 281 songs, but parsed " + str(counter_songs))
        self.assertEqual(427, counter_writers, msg="Expected 427 songs with writter, but parsed " + str(counter_writers))


    def test_many_real_songs(self):
        parser = DiscogsSongParser(file_path=rel_path_to_file("../../files/discogs_releases.xml", __file__),
                                   dataset=Dataset(title="TestDataset"))

        counter = 1
        for a_song in parser.parse_songs():
            counter += 1
            if counter % 50000 == 0:  # 50.000
                break



