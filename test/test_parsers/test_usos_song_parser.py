__author__ = 'Dani'

import unittest

from wmera.mera_core.model.entities import Dataset
from wmera.parsers.usos.usos_song_parser import UsosSongParser
from wmera.utils import rel_path_to_file


class TestUsosSongParser(unittest.TestCase):
    def test_titles_detection(self):
        parser = UsosSongParser(dataset=Dataset("some_dataset"),
                                source_file=rel_path_to_file("../../files/in/mini_uso.tsv", __file__))
        expected_dict = {
            "kentucky woman": False,
            "why tell me why": False,
            "acapella": False,
            "human": False,
            "carry out": False,
            "don't stop the party": False,
            "whistle": False,
            "somebody that i used to know": False
        }
        unexpected = []
        for song in parser.parse_songs():
            if song.canonical.strip() in expected_dict:
                expected_dict[song.canonical.strip()] = True
            else:
                unexpected.append(song.canonical)
        self.assertEquals(0, len(unexpected), "Some unexpected songs where parsed: " + str(unexpected))
        not_found = []
        for a_expected in expected_dict:
            if not expected_dict[a_expected]:
                not_found.append(a_expected)
        self.assertEquals(0, len(not_found), "Some expected songs were not found: " + str(not_found))


    def test_artist_detection(self):
        parser = UsosSongParser(dataset=Dataset("some_dataset"),
                                source_file=rel_path_to_file("../../files/in/mini_uso.tsv", __file__))
        expected_dict = {
            "Neil Diamond": False,
            "Anita Meyer": False,
            "Karmin": False,
            "The Killers": False,
            "Justin Timberlake": False,
            "Timbaland": False,
            "The Black Eyed Peas": False,
            "Flo Rida": False,
            "Gotye": False
        }
        unexpected = []
        for song in parser.parse_songs():
            for artist in song.artists:
                if artist.canonical.strip() in expected_dict:
                    expected_dict[artist.canonical.strip()] = True
                else:
                    unexpected.append(artist.canonical)
        self.assertEquals(0, len(unexpected), "Some unexpected artists where parsed: " + str(unexpected))
        not_found = []
        for a_expected in expected_dict:
            if not expected_dict[a_expected]:
                not_found.append(a_expected)
        self.assertEquals(0, len(not_found), "Some expected artist were not found: " + str(not_found))



    def test_writers_detection(self):
        parser = UsosSongParser(dataset=Dataset("some_dataset"),
                                source_file=rel_path_to_file("../../files/in/mini_uso.tsv", __file__))
        expected_dict = {
            "Amy Heidemann": False,
            "Martin Johnson": False,
            "Nick Noonan": False,
            "Sam Hollander": False,
            "Brandon Flowers": False,
            "Dave Keuning": False,
            "Ronnie Vannucci": False,
            "Jerome Harmon": False,
            "Jim Beanz": False,
            "Justin Timberlake": False,
            "Timothy Clayton": False,
            "Timothy Mosley": False,
            "Backer": False,
            "Wally De": False
        }
        unexpected = []
        for song in parser.parse_songs():
            for a_coll in song.collaborations:
                if a_coll.collaborator.canonical.strip() in expected_dict:
                    expected_dict[a_coll.collaborator.canonical.strip()] = True
                else:
                    unexpected.append(a_coll.collaborator.canonical)
        self.assertEquals(0, len(unexpected), "Some unexpected writers where parsed: " + str(unexpected))
        not_found = []
        for a_expected in expected_dict:
            if not expected_dict[a_expected]:
                not_found.append(a_expected)
        self.assertEquals(0, len(not_found), "Some expected writers were not found: " + str(not_found))


    def test_entity_detection(self):
        parser = UsosSongParser(dataset=Dataset("some_dataset"),
                                source_file=rel_path_to_file("../../files/in/mini_uso.tsv", __file__))
        counter = 0
        for song in parser.parse_songs():
            counter += 1
        self.assertEquals(8, counter, "Unexpected number of songs. Expected 8 bur parsed " + str(counter))



    def test_many_songs_parsed(self):
        parser = UsosSongParser(dataset=Dataset("some_dataset"),
                                source_file=rel_path_to_file("../../files/in/bmat2heaven.tsv", __file__))

        counter = 50000
        for a_song in parser.parse_songs():
            counter -= 1
            if counter <= 0:
                break
        # I just want to check that no error happens when we parse many songs

