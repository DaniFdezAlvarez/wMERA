from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples

__author__ = 'Dani'


from wmera.graph_gen.rdflib.graph_generator import GraphGenerator
from wmera.graph_gen.rdflib.entities_gen.song_to_triples_uri_known import SongToTriplesUriKnown
from wmera.graph_gen.rdflib.entities_gen.artist_to_triples import ArtistToTriples



class GraphGeneratorSongUriKnown(GraphGenerator):

    def run_song_gen(self, song_parser, isolated=False):
        """
        It return a graph containing all the info of the song_parser. If
        grpah is None, it will return a new graph. Otherwise, it will return
        the received graph with the new info.

        :param song_parser:
        :return:
        """

        dataset_to_triples = DatasetToTriples(graph=self._mera_graph, matcher=self._mera_matcher)

        return SongToTriplesUriKnown(graph=self._mera_graph,
                                     ngram_repo=self._repo_songs,
                                     artist_to_triples=ArtistToTriples(graph=self._mera_graph,
                                                                       ngram_repo=self._repo_artists,
                                                                       dataset_to_triples=dataset_to_triples,
                                                                       entity_counter_repo=self._repo_counter,
                                                                       matcher=self._mera_matcher),
                                     dataset_to_triples=dataset_to_triples,
                                     entity_counter_repo=self._repo_counter,
                                     matcher=self._mera_matcher). \
            add_song_triples_to_graph(song_parser)