from apps.building_graph.parsers.discogs_song_parser_filtering import DiscogsSongParserFiltering

__author__ = 'Dani'

from apps.building_graph.generators.generator_persisting_artists import GraphGeneratorPersistingArtist
from wmera.graph_gen.rdflib.mera_impl.mera_rdflib_graph import MeraRdflibGraph
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
from wmera.infrastrusture.in_memory.memory_entity_counter import MemoryEntityCounter
from wmera.infrastrusture.in_memory.memory_entity_ngrams import MemoryEntityNgrams
from wmera.mera_core.mera_infrastructure.entity_ngrams_interface import ARTIST_COLLECTION, SONG_COLLECTION
from wmera.mera_core.mera_matcher.mera_matcher import MeraMatcher
from apps.building_graph.parsers.discogs_song_parser_artist_id_detection import DiscogsSongParserArtistIdDetection
from apps.building_graph.parsers.discogs_artist_parser_filtering import DiscogsArtistParserFiltering
from wmera.mera_core.model.entities import Dataset
from rdflib import Graph


def read_necessary_index_songs(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        for line in file_io:
            line = line.replace("\n", "")
            if line != "":
                result.add(int(line))
    return result


preliminar_set_of_songs = read_necessary_index_songs("files/all_discogs_indexes.txt")
fake_set_of_artist = set()
fake_set_of_artist.add(1)
fake_set_of_artist.add(2)
fake_set_of_artist.add(3)
fake_set_of_artist.add(29)
fake_set_of_artist.add(26)
fake_set_of_artist.add(27)

dataset = Dataset(title="selected_discogs_indexes")
# "../../files/discogs_releases.xml"
artist_parser = DiscogsArtistParserFiltering("../../files/discogs_artists.xml",
                                             dataset,
                                             fake_set_of_artist)
graph = MeraRdflibGraph(rdflib_graph=Graph())
artist_ngrams = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                   type_of_entity_collection=ARTIST_COLLECTION)
song_ngrams = MemoryEntityNgrams(base_entity_uri=base_entities_URI,
                                 type_of_entity_collection=SONG_COLLECTION)
counter = MemoryEntityCounter()
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
fake_song_set = set()
for i in range(1, 10):
    fake_song_set.add(i)
song_parser = DiscogsSongParserFiltering(file_path="../../files/discogs_releases.xml",
                                         target_indexes=fake_song_set,
                                         dataset=dataset)

generator.generate_turtle_artist_graph("files/mini_artist.ttl", artist_parser=artist_parser)
generator.generate_turtle_song_graph("files/mini_complete_graph.ttl", song_parser=song_parser, isolated=True)

