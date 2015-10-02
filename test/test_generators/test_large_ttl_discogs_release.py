__author__ = 'Dani'

import unittest

from wmera.parsers.discogs.song_parser import DiscogsSongParser
from wmera.mera_core.model.entities import Dataset
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos
from wmera.utils import rel_path_to_file


class TestGenerateLargeTtlDiscogsRelease(unittest.TestCase):
    def test_generate(self):
        dataset = Dataset("A fancy dataset")
        parser = DiscogsSongParser(file_path=rel_path_to_file("../../files/releases_piece_small.xml", __file__),
                                   dataset=dataset)

        generator = get_clean_graph_generator_mongo_repos()
        generator.generate_turtle_song_graph(
            file_path=rel_path_to_file("../../files/out/large_discogs_release.ttl", __file__),
            song_parser=parser)


