__author__ = 'Dani'

import unittest

from wmera.mera_core.model.entities import Dataset
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos
from test.t_utils.fake_parsers import FakeArtistParser
from wmera.utils import rel_path_to_file



class TestGenerateArtistFake(unittest.TestCase):
    def test_generate_artist_fake(self):
        file_path = rel_path_to_file("../../files/artist_mini_graph.ttl", __file__)
        artist_parser = FakeArtistParser(Dataset("MyTest", date="2000-feb-15"))
        generator = get_clean_graph_generator_mongo_repos()
        generator.generate_turtle_artist_graph(file_path=file_path, artist_parser=artist_parser)