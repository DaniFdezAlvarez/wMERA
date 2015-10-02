from wmera.graph_gen.rdflib.mera_impl.mera_rdflib_graph import MeraRdflibGraph

__author__ = 'Dani'

from rdflib import Graph

from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import bind_namespaces
from wmera.graph_gen.rdflib.entities_gen.artist_to_triples import ArtistToTriples
from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples
from wmera.graph_gen.rdflib.entities_gen.song_to_triples import SongToTriples
from wmera.infrastrusture.mongo.ngrams.mongo_entity_ngrams import MongoEntityNgramsRepository, ARTIST_COLLECTION, \
    SONG_COLLECTION
from wmera.infrastrusture.mongo.entity_counter.mongo_entity_counter import EntityCounterRepositoryMongo
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
from wmera.mera_core.mera_matcher.mera_matcher import MeraMatcher


class GraphGenerator(object):
    def __init__(self, mera_graph=None, repo_artist=None, repo_songs=None, repo_counter=None, mera_matcher=None):
        mera_graph, repo_songs, repo_artists, repo_counter, mera_matcher = GraphGenerator. \
            initialize_structures_if_needed(graph=mera_graph,
                                            repo_songs=repo_songs,
                                            repo_artists=repo_artist,
                                            repo_counter=repo_counter,
                                            matcher=mera_matcher)
        self._mera_graph = mera_graph
        self._repo_songs = repo_songs
        self._repo_artists = repo_artists
        self._repo_counter = repo_counter
        self._mera_matcher = mera_matcher


    def generate_turtle_graph(self, file_path, artist_parser=None, song_parser=None):
        if artist_parser is None and song_parser is None:
            raise ValueError("You must provide at least a parser")

        self._mera_graph = self.generate_mera_graph(artist_parser=artist_parser,
                                                    song_parser=song_parser)
        self.write_graph_to_turtle_file(file_path=file_path)


    def generate_mera_graph(self, artist_parser=None, song_parser=None):

        if artist_parser is None and song_parser is None:
            raise ValueError("You must provide at least a parser")

        if artist_parser is not None:
            self._mera_graph = self.run_artist_gen(artist_parser=artist_parser)

        if song_parser is not None:
            self._mera_graph = self.run_song_gen(song_parser=song_parser)

        return self._mera_graph


    def generate_turtle_song_graph(self, file_path, song_parser, isolated=False):
        self._mera_graph = self.run_song_gen(song_parser=song_parser, isolated=isolated)
        self.write_graph_to_turtle_file(file_path=file_path)


    def run_artist_gen(self, artist_parser):
        """
        It returns a graph containing all the info of the artist_parser. If
        graph is None, it will return a new graph. Otherwise, it will return the received graph with the
        new info.

        :param artist_parser:
        :return:
        """

        return ArtistToTriples(graph=self._mera_graph,
                               ngram_repo=self._repo_artists,
                               dataset_to_triples=DatasetToTriples(graph=self._mera_graph, matcher=self._mera_matcher),
                               entity_counter_repo=self._repo_counter, matcher=self._mera_matcher). \
            add_artists_triples_to_graph(artist_parser)


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
            return SongToTriples(graph=self._mera_graph,
                                 ngram_repo=self._repo_songs,
                                 artist_to_triples=ArtistToTriples(graph=self._mera_graph,
                                                                   ngram_repo=self._repo_artists,
                                                                   dataset_to_triples=dataset_to_triples,
                                                                   entity_counter_repo=self._repo_counter,
                                                                   matcher=self._mera_matcher),
                                 dataset_to_triples=dataset_to_triples,
                                 entity_counter_repo=self._repo_counter,
                                 matcher=self._mera_matcher).add_song_triples_of_isolated_nodes_to_graph(song_parser)

        return SongToTriples(graph=self._mera_graph,
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


    def write_graph_to_turtle_file(self, file_path):
        serialized = self._mera_graph.serialize(out_format='turtle')
        with open(file_path, 'w') as dataset:
            dataset.write(serialized)


    def generate_turtle_artist_graph(self, file_path, artist_parser):
        self._mera_graph = self.run_artist_gen(artist_parser=artist_parser)
        self.write_graph_to_turtle_file(file_path=file_path)


    @staticmethod
    def initialize_structures_if_needed(graph, repo_songs, repo_artists, repo_counter, matcher):
        if graph is None:
            graph = Graph()
            bind_namespaces(graph)
            graph = MeraRdflibGraph(graph)
        if repo_artists is None:
            repo_artists = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
                                                       base_entity_uri=base_entities_URI,
                                                       type_of_entity_collection=ARTIST_COLLECTION)
        if repo_songs is None:
            repo_songs = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
                                                     base_entity_uri=base_entities_URI,
                                                     type_of_entity_collection=SONG_COLLECTION)

        if repo_counter is None:
            repo_counter = EntityCounterRepositoryMongo(url_root="127.0.0.1:27017",
                                                        collection="entities_count")

        if matcher is None:
            matcher = MeraMatcher(graph=graph,
                                  artist_ngrams_repository=repo_artists,
                                  song_ngrams_repository=repo_songs,
                                  entity_counter_repository=repo_counter)

        return graph, repo_songs, repo_artists, repo_counter, matcher
