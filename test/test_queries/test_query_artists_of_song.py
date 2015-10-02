__author__ = 'Dani'

import unittest

from test.test_generators.test_graph_songs import FakeSongParser
from test.test_generators.test_graph_artist import FakeArtistParser
from wmera.mera_core.model.entities import Dataset
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
from wmera.graph_gen.rdflib.rdf_utils.queries import Queries
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos


class TestQueryArtistOfSong(unittest.TestCase):

    def test_query_artist_of_song(self):

        dataset = Dataset("A fancy dataset")
        generator = get_clean_graph_generator_mongo_repos()
        mera_graph = generator.generate_mera_graph(artist_parser=FakeArtistParser(dataset),
                                                   song_parser=FakeSongParser(dataset))
        rdflib_graph = mera_graph._graph

        rows = rdflib_graph.query(Queries.find_artists_uri_compiled(base_entities_URI + "avaloncho"))

        counter = 0
        last_result = ""
        for row in rows:
            counter += 1
            last_result = str(row[0])

        self.assertEquals(counter, 1)
        self.assertEquals(last_result, base_entities_URI + "herroes_del_selencio")



