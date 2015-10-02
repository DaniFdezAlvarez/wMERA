__author__ = 'Dani'

from apps.building_graph.generators.generator_persisting_artists import GraphGeneratorPersistingArtist
from wmera.graph_gen.rdflib.mera_impl.mera_rdflib_graph import MeraRdflibGraph
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
# from wmera.infrastrusture.mongo.ngrams.mongo_entity_ngrams import MongoEntityNgramsRepository
# from wmera.infrastrusture.mongo.entity_counter.mongo_entity_counter import EntityCounterRepositoryMongo
from wmera.mera_core.mera_infrastructure.entity_ngrams_interface import ARTIST_COLLECTION, SONG_COLLECTION
from wmera.infrastrusture.in_memory.memory_entity_counter import MemoryEntityCounter
from wmera.infrastrusture.in_memory.memory_entity_ngrams import MemoryEntityNgrams
from wmera.mera_core.mera_matcher.mera_matcher import MeraMatcher
from apps.building_graph.parsers.discogs_artist_parser_filtering import DiscogsArtistParserFiltering
from apps.building_graph.parsers.discogs_song_parser_filtering import DiscogsSongParserFiltering
from wmera.mera_core.model.entities import Dataset
from apps.building_graph.parsers.discogs_artist_parser_filtering_no_namevars import \
    DiscogsArtistParserFilteringNoNamevars
from apps.building_graph.parsers.discogs_song_parser_filtering_no_namevars import DiscogsSongParserFilteringNoNamevars
from rdflib import Graph


def read_necessary_index_songs(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        for line in file_io:
            line = line.replace("\n", "")
            if line != "":
                result.add(int(line))
    return result


def read_aol_discogs_ids(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        file_io.readline()  # discard heading
        for line in file_io:
            line = line.replace("\n", "")
            pieces = line.split("\t")
            if pieces[-1] != "":
                result.add(pieces[-1])
    return result


def read_mb_discogs_ids(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        file_io.readline()  # discard heading
        for line in file_io:
            pieces = line.split("\t")
            if pieces[1] != "":
                result.add(pieces[1])
    return result


# preliminar_set_of_songs = read_necessary_index_songs("files/all_discogs_indexes.txt")
set_of_songs = read_necessary_index_songs("files/500000_discogs_song_indexes.txt")
set_of_artist = read_necessary_index_songs("files/artists_indexes_for_500000_discogs_songs.txt")

set_of_ids_aol = read_aol_discogs_ids("files/random_aol.txt")
set_of_musicbrainz_ids = read_mb_discogs_ids("files/random_musicbrainz.tsv")

ip_mongo = "127.0.0.1"
port_mongo = 27017
path_mongo = ip_mongo + ":" + str(port_mongo)

dataset = Dataset(title="selected_discogs_indexes")
artist_parser = DiscogsArtistParserFiltering("files/discogs_artists.xml",
                                             dataset,
                                             set_of_artist)
graph = MeraRdflibGraph(rdflib_graph=Graph())
artist_ngrams = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                   type_of_entity_collection=ARTIST_COLLECTION,
                                   load_file=None)
song_ngrams = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                 type_of_entity_collection=SONG_COLLECTION,
                                 load_file=None)
counter = MemoryEntityCounter()
# artist_ngrams = MongoEntityNgramsRepository(base_entity_uri=base_entities_URI,
# type_of_entity_collection=ARTIST_COLLECTION,
# url_root=path_mongo,
# host=ip_mongo,
# port=port_mongo)
# song_ngrams = MongoEntityNgramsRepository(base_entity_uri=base_entities_URI,
# type_of_entity_collection=SONG_COLLECTION,
# url_root=path_mongo,
#                                           host=ip_mongo,
#                                           port=port_mongo)
# counter = EntityCounterRepositoryMongo(url_root=path_mongo,
#                                        host=ip_mongo,
#                                        port=port_mongo,
#                                        collection="entities_count")
matcher = MeraMatcher(graph=graph,
                      artist_ngrams_repository=artist_ngrams,
                      song_ngrams_repository=song_ngrams,
                      entity_counter_repository=counter)

generator = GraphGeneratorPersistingArtist(mera_graph=graph,
                                           repo_artist=artist_ngrams,
                                           repo_songs=song_ngrams,
                                           repo_counter=counter,
                                           mera_matcher=matcher,
                                           file_path_index_artist="files/little_artist_index_dict.txt")
song_parser = DiscogsSongParserFiltering(file_path="files/discogs_releases.xml",
                                         target_indexes=set_of_songs,
                                         dataset=dataset,
                                         target_ids=set_of_ids_aol.union(set_of_musicbrainz_ids))
print "Starting artists generators...."
generator.generate_turtle_artist_graph("files/artist.ttl", artist_parser=artist_parser)
artist_ngrams.save_content("files/artist_stage_artist_ngrams.json")
song_ngrams.save_content("files/artist_stage_song_ngrams.json")
counter.save_content("files/artsit_stage_counter.json")
print "Artists complete, strating song generators...."
generator.generate_turtle_song_graph("files/complete_graph.ttl", song_parser=song_parser, isolated=True)
artist_ngrams.save_content("files/final_stage_artist_ngrams.json")
song_ngrams.save_content("files/final_stage_song_ngrams.json")
counter.save_content("files/final_stage_counter.json")

