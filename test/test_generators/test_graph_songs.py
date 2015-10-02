# coding=utf-8
__author__ = 'Dani'

import unittest

from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos
from test.t_utils.fake_parsers import FakeSongParser
from wmera.mera_core.model.entities import Dataset
from wmera.utils import rel_path_to_file




# ##########   TEST


class TestGenerateSong(unittest.TestCase):
    def test_generate_song(self):
        generator = get_clean_graph_generator_mongo_repos()
        generator.generate_turtle_song_graph(file_path=rel_path_to_file("../../files/out/test_song_gen.ttl", __file__),
                                             song_parser=FakeSongParser(dataset=Dataset("A_Dataset")))



