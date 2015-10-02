__author__ = 'Dani'

import json

from rdflib import Graph

from controller.query_executer import QueryExecuter
from wmera.controller.formater_to_json import FormaterToJson
from wmera.mera_core.mera_matcher.mera_matcher import MeraMatcher
from wmera.utils import rel_path_to_file
from wmera.graph_gen.rdflib.mera_impl.mera_rdflib_graph import MeraRdflibGraph
from infrastrusture.in_memory.memory_entity_ngrams import MemoryEntityNgrams, ARTIST_COLLECTION, SONG_COLLECTION
from infrastrusture.in_memory.memory_entity_counter import MemoryEntityCounter
from wmera.infrastrusture.mongo.entity_counter.mongo_entity_counter import EntityCounterRepositoryMongo
from wmera.infrastrusture.mongo.ngrams.mongo_entity_ngrams import MongoEntityNgramsRepository
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
from wmera.mera_core.mera_matcher.json_to_match_config import translate_json_to_mera_match_config


def get_executer_memory_repos_file_rdflib_graph(str_json_config):
    print "loading graph"
    #Graph from file
    graph_path = rel_path_to_file("files/mini_usos/mini_usos_graph.ttl", __file__)
    rdflib_graph = Graph()
    rdflib_graph.load(graph_path, format="turtle")
    mera_graph = MeraRdflibGraph(rdflib_graph)

    print "loading artist ngrams"
    #Memory artist repo from file
    artist_ngram_path = rel_path_to_file("files/mini_usos/artist.json", __file__)
    repo_artist = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                     type_of_entity_collection=ARTIST_COLLECTION,
                                     load_file=artist_ngram_path)

    print "loading songs ngrams"
    #Memory song repo from file
    song_ngram_path = rel_path_to_file("files/mini_usos/song.json", __file__)
    repo_song = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                   type_of_entity_collection=SONG_COLLECTION,
                                   load_file=song_ngram_path)

    print "loading repo counter"
    #Memory counter repo from file
    counter_path = rel_path_to_file("files/mini_usos/counter.json", __file__)
    repo_counter = MemoryEntityCounter(load_file=counter_path)

    print "Loading matcher"
    #Matcher over those structures
    matcher = MeraMatcher(graph=mera_graph,
                          artist_ngrams_repository=repo_artist,
                          song_ngrams_repository=repo_song,
                          entity_counter_repository=repo_counter,
                          match_config=translate_json_to_mera_match_config(json.loads(str_json_config)))

    #Formater to json
    formater = FormaterToJson()

    print "loading executer"
    #Executer over those structures
    executer = QueryExecuter(matcher=matcher,
                             formater=formater)

    return executer


def get_memory_graph(graph_path):
    rdflib_graph = Graph()
    rdflib_graph.load(graph_path, format="turtle")
    return MeraRdflibGraph(rdflib_graph)


def get_executer_mongo_obj(str_json_config, ip_mongo, port_mongo, mera_graph):
    path_mongo = ip_mongo + ":" + str(port_mongo)




    artists_ngram_repo = MongoEntityNgramsRepository(url_root=path_mongo,
                                                     base_entity_uri=base_entities_URI,
                                                     type_of_entity_collection=ARTIST_COLLECTION,
                                                     host=ip_mongo,
                                                     port=port_mongo)

    songs_ngram_repo = MongoEntityNgramsRepository(url_root=path_mongo,
                                                   base_entity_uri=base_entities_URI,
                                                   type_of_entity_collection=SONG_COLLECTION,
                                                   host=ip_mongo,
                                                   port=port_mongo)

    entity_counter_repo = EntityCounterRepositoryMongo(url_root=path_mongo,
                                                       collection="entities_count",
                                                       host=ip_mongo,
                                                       port=port_mongo)

    #Matcher over those structures
    matcher = MeraMatcher(graph=mera_graph,
                          artist_ngrams_repository=artists_ngram_repo,
                          song_ngrams_repository=songs_ngram_repo,
                          entity_counter_repository=entity_counter_repo,
                          match_config=translate_json_to_mera_match_config(json.loads(str_json_config)))

    #Formater to json
    formater = FormaterToJson()

    # print "loading executer"
    #Executer over those structures
    executer = QueryExecuter(matcher=matcher,
                             formater=formater)

    return executer



