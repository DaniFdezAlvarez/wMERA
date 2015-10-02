from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples

__author__ = 'Dani'

from wmera.graph_gen.rdflib.graph_generator import GraphGenerator
from apps.building_graph.generators.artist_to_triples_persisting_index_uris import ArtistToTriplesPersistingIndexUris
from apps.building_graph.generators.song_to_triples_artist_index import SongToTriplesArtistIndex


class GraphGeneratorPersistingArtist(GraphGenerator):
    """
    Uses ArtistToTriplesPersistingIndexUris and SongToTriplesArtistIndex

    """

    def __init__(self, file_path_index_artist, mera_graph=None, repo_artist=None, repo_songs=None,
                 repo_counter=None, mera_matcher=None):
        super(GraphGeneratorPersistingArtist, self).__init__(mera_graph, repo_artist, repo_songs,
                                                             repo_counter, mera_matcher)
        self._path_persist_artist = file_path_index_artist


    def run_artist_gen(self, artist_parser):
        """
        It returns a graph containing all the info of the artist_parser. If
        graph is None, it will return a new graph. Otherwise, it will return the received graph with the
        new info.

        :param artist_parser:
        :return:
        """
        artist_to_triples = ArtistToTriplesPersistingIndexUris(graph=self._mera_graph,
                                                               ngram_repo=self._repo_artists,
                                                               dataset_to_triples=DatasetToTriples(
                                                                   graph=self._mera_graph,
                                                                   matcher=self._mera_matcher),
                                                               entity_counter_repo=self._repo_counter,
                                                               matcher=self._mera_matcher,
                                                               file_path_dict=self._path_persist_artist,
                                                               reset_file_path=True)

        result = artist_to_triples.add_artists_triples_to_graph(artist_parser)
        return result


    def run_song_gen(self, song_parser, isolated=False):
        """
        It return a graph containing all the info of the song_parser. If
        grpah is None, it will return a new graph. Otherwise, it will return
        the received graph with the new info.

        :param song_parser:
        :return:
        """

        dataset_to_triples = DatasetToTriples(graph=self._mera_graph, matcher=self._mera_matcher)

        if isolated:
            return SongToTriplesArtistIndex(graph=self._mera_graph,
                                            ngram_repo=self._repo_songs,
                                            artist_to_triples=None,
                                            dataset_to_triples=dataset_to_triples,
                                            entity_counter_repo=self._repo_counter,
                                            matcher=self._mera_matcher,
                                            file_path_dict=self._path_persist_artist). \
                add_song_triples_of_isolated_nodes_to_graph(song_parser)

        return SongToTriplesArtistIndex(graph=self._mera_graph,
                                        ngram_repo=self._repo_songs,
                                        artist_to_triples=None,
                                        dataset_to_triples=dataset_to_triples,
                                        entity_counter_repo=self._repo_counter,
                                        matcher=self._mera_matcher,
                                        file_path_dict=self._path_persist_artist). \
            add_song_triples_to_graph(song_parser)

