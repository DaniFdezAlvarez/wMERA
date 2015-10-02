__author__ = 'Dani'

import unittest

from test.test_generators.test_graph_songs import FakeSongParser
from test.test_generators.test_graph_artist import FakeArtistParser
from wmera.mera_core.model.entities import Dataset
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos


class TestCombinedQueries(unittest.TestCase):
    def test_song_with_artist(self):
        generator = get_clean_graph_generator_mongo_repos()
        dataset = Dataset("A fancy dataset")
        mera_graph = generator.generate_mera_graph(artist_parser=FakeArtistParser(dataset),
                                                   song_parser=FakeSongParser(dataset))
        matcher = generator._mera_matcher

        results = matcher.find_song(name="Avaloncho", artists=["Perry Mason"])

        self.assertEquals(2, len(results))
        self.assertEquals('Avalincho', results[0].entity.canonical)
        print "1st:", results[0].entity.canonical
        print "2nd", results[1].entity.canonical