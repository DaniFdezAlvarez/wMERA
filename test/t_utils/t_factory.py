from rdflib import Graph

from wmera.graph_gen.rdflib.graph_generator import GraphGenerator
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
from wmera.infrastrusture.mongo.entity_counter.mongo_entity_counter import EntityCounterRepositoryMongo
from wmera.infrastrusture.mongo.ngrams.mongo_entity_ngrams import MongoEntityNgramsRepository
from wmera.mera_core.mera_infrastructure.entity_ngrams_interface import ARTIST_COLLECTION, SONG_COLLECTION
from wmera.infrastrusture.in_memory.memory_entity_counter import MemoryEntityCounter
from wmera.infrastrusture.in_memory.memory_entity_ngrams import MemoryEntityNgrams
from wmera.graph_gen.rdflib.mera_impl.mera_rdflib_graph import MeraRdflibGraph
from wmera.mera_core.mera_matcher.mera_matcher import MeraMatcher


__author__ = 'Dani'


def get_clean_graph_generator_memory_repos():
    artists_ngram_repo = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                            type_of_entity_collection=ARTIST_COLLECTION)
    songs_ngram_repo = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                          type_of_entity_collection=SONG_COLLECTION)
    entity_counter_repo = MemoryEntityCounter()

    songs_ngram_repo.reset_collection()
    artists_ngram_repo.reset_collection()
    entity_counter_repo.reset_count()

    return GraphGenerator(repo_songs=songs_ngram_repo,
                          repo_artist=artists_ngram_repo,
                          repo_counter=entity_counter_repo)


def get_clean_graph_generator_mongo_repos():
    artists_ngram_repo = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
                                                     base_entity_uri=base_entities_URI,
                                                     type_of_entity_collection=ARTIST_COLLECTION)

    songs_ngram_repo = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
                                                   base_entity_uri=base_entities_URI,
                                                   type_of_entity_collection=SONG_COLLECTION)

    entity_counter_repo = EntityCounterRepositoryMongo(url_root="127.0.0.1:27017",
                                                       collection="entities_count")

    songs_ngram_repo.reset_collection()
    artists_ngram_repo.reset_collection()
    entity_counter_repo.reset_count()

    return GraphGenerator(repo_songs=songs_ngram_repo,
                          repo_artist=artists_ngram_repo,
                          repo_counter=entity_counter_repo)


def get_clean_repo_artist_mongo():
    artists_ngram_repo = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
                                                     base_entity_uri=base_entities_URI,
                                                     type_of_entity_collection=ARTIST_COLLECTION)
    artists_ngram_repo.reset_collection()
    return artists_ngram_repo


def get_clean_repo_songs_mongo():
    songs_ngram_repo = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
                                                   base_entity_uri=base_entities_URI,
                                                   type_of_entity_collection=SONG_COLLECTION)
    songs_ngram_repo.reset_collection()
    return songs_ngram_repo


def get_clean_repo_counter_mongo():
    entity_counter_repo = EntityCounterRepositoryMongo(url_root="127.0.0.1:27017",
                                                       collection="entities_count")
    entity_counter_repo.reset_count()
    return entity_counter_repo


def get_clean_repo_artist_memory():
    return MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                              type_of_entity_collection=ARTIST_COLLECTION)


def get_clean_repo_counter_memory():
    return MemoryEntityCounter()


def get_clean_repo_song_memory():
    return MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                              type_of_entity_collection=SONG_COLLECTION)


def get_clean_MeraRdflibGraph():
    return MeraRdflibGraph(rdflib_graph=Graph())


def get_empty_mera_matcher():
    return MeraMatcher(graph=get_clean_MeraRdflibGraph(),
                       artist_ngrams_repository=get_clean_repo_artist_memory(),
                       song_ngrams_repository=get_clean_repo_song_memory(),
                       entity_counter_repository=get_clean_repo_counter_memory())


def get_mera_matcher_with_data(graph_path, ngram_song_path, ngram_artist_path, counter_path):
    rdf_lib_graph = Graph()
    rdf_lib_graph.load(graph_path, format="turtle")
    mera_graph = MeraRdflibGraph(rdf_lib_graph)

    artist_ngram = get_clean_repo_artist_memory()
    artist_ngram.load_content(ngram_artist_path)

    song_ngram = get_clean_repo_song_memory()
    song_ngram.load_content(ngram_song_path)

    counter = get_clean_repo_counter_memory()
    counter.load_content(counter_path)


    return MeraMatcher(graph=mera_graph,
                       artist_ngrams_repository=artist_ngram,
                       song_ngrams_repository=song_ngram,
                       entity_counter_repository=counter)




