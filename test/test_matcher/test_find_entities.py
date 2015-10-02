__author__ = 'Dani'

import unittest

from test.test_generators.test_graph_songs import FakeSongParser
from test.test_generators.test_graph_artist import FakeArtistParser
from wmera.mera_core.model.entities import Dataset
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos, get_mera_matcher_with_data
from wmera.graph_gen.rdflib.mera_impl.mera_rdflib_graph import MeraRdflibGraph
from rdflib import Graph
from wmera.utils import rel_path_to_file
# from controller.formater_to_json import FormaterToJson


class TestFindEntities(unittest.TestCase):
    def test_find_entities(self):
        dataset = Dataset("A fancy dataset")
        generator = get_clean_graph_generator_mongo_repos()
        mera_graph = generator.generate_mera_graph(artist_parser=FakeArtistParser(dataset),
                                                   song_parser=FakeSongParser(dataset))
        matcher = generator._mera_matcher

        matcher._match_config._default_threshold = 0.60  ## All OK, This is a test

        results = matcher.find_artist(name="Heroes del Silencio")
        self.assertEquals("Herroes del selencio", results[0].entity.canonical)

        results = matcher.find_song("Avalincha")
        self.assertEquals("Avalincho", results[0].entity.canonical)

        results = matcher.find_song("Avaloncha")
        self.assertEquals("Avaloncho", results[0].entity.canonical)

        results = matcher.find_song("Amor de no verano")
        self.assertEquals("Amor de verano", results[0].entity.canonical)

    def test_find_entities_usos(self):
        matcher = get_mera_matcher_with_data(graph_path=rel_path_to_file("../../files/out/usos_graph.ttl",
                                                                         __file__),
                                             ngram_artist_path=rel_path_to_file(
                                                 "../../files/out/artist_ngrams_usos.json",
                                                 __file__),
                                             ngram_song_path=rel_path_to_file("../../files/out/song_ngrams_usos.json",
                                                                              __file__),
                                             counter_path=rel_path_to_file("../../files/out/counter_usos.json",
                                                                           __file__))
        results = matcher.find_song("Carry out")
        self.assertEquals("carry out", results[0].entity.canonical)
        self.assertEquals("USUM70915229", results[0].entity.usos_isrc)
        self.assertEquals("5", results[0].entity.usos_transaction_id)

