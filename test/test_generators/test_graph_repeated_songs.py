import unittest

from wmera.utils import rel_path_to_file
from wmera.mera_core.model.entities import Dataset
from test.t_utils.fake_parsers import FakeRepeatedSongParser
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos


__author__ = 'Dani'


class TestGraphRepeatedSongs(unittest.TestCase):

    def test_graph_repeated_songs(self):
        file_path = rel_path_to_file("../../files/out/repeated_song_mini_graph.ttl", __file__)
        song_parser = FakeRepeatedSongParser(Dataset("MyTest", date="2000-feb-15"))
        generator = get_clean_graph_generator_mongo_repos()
        generator.generate_turtle_song_graph(file_path, song_parser)
