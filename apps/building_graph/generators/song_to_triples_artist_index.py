from wmera.graph_gen.rdflib.index_utils.entity_counter_utils import increase_song_count
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import *
from rdflib.namespace import RDF, FOAF

__author__ = 'Dani'


from wmera.graph_gen.rdflib.entities_gen.song_to_triples import SongToTriples


class SongToTriplesArtistIndex(SongToTriples):

    def __init__(self, graph, ngram_repo, artist_to_triples, dataset_to_triples, entity_counter_repo,
                 matcher, file_path_dict):
        super(SongToTriplesArtistIndex, self).__init__(graph, ngram_repo, artist_to_triples,
                                                       dataset_to_triples,
                                                       entity_counter_repo, matcher)
        self._file_path_dict = file_path_dict
        self._index_artist = self._load_artist_index()



    def _load_artist_index(self):
        result = {}
        with open(self._file_path_dict, "r") as file_io:
            for line in file_io:
                line = line[:-1]  # Removing "\n" char
                pieces = line.split("|")
                result[int(pieces[0])] = pieces[1]
        return result


    def _generate_triples_for_new_song(self, song, dataset_uri, isolated_song=False):
        song_uri = self.generate_entity_uri(entity=song,
                                            alt_str=SongToTriples.prepare_alt_str_for_song(song))
        # # triple of type
        yield (song_uri, RDF.type, MO.track)

        # # canonical
        for triple in SongToTriples._generate_canonical_triples(song, song_uri, dataset_uri,
                                                                self._ngram_repo):
            yield triple


        # # Triples of the artists
        for artist in song.artists:
            if artist.discogs_id in self._index_artist:
                yield (song_uri, FOAF.maker, URIRef(self._index_artist[artist.discogs_id]))
        for collaboration in song.collaborations:
            if collaboration.collaborator.discogs_id in self._index_artist:
                yield (song_uri, FOAF.maker, URIRef(self._index_artist[collaboration.collaborator.discogs_id]))


        # # Alternative titles
        for triple in SongToTriples._generate_alt_titles_triples_of_song(song=song,
                                                                         song_uri=song_uri,
                                                                         dataset_uri=dataset_uri,
                                                                         ngram_repo=self._ngram_repo,
        ):
            yield triple

        # #  Country
        if song.country is not None:
            for triple in SongToTriples._generate_country_triples(entity=song,
                                                                  entity_uri=song_uri,
                                                                  dataset_uri=dataset_uri):
                yield triple

        ## Discogs elems
        if song.discogs_id is not None:
            for triple in SongToTriples._generate_discogs_id_triples(entity=song,
                                                                     entity_uri=song_uri):
                yield triple

        if song.discogs_index is not None:
            for triple in SongToTriples._generate_discogs_index_triples(entity=song,
                                                                        entity_uri=song_uri):
                yield triple


        increase_song_count(entity_counter_repo=self._entity_counter_repo)

        # TODO The next are still not implemented
        # :param collaborations: list of collaboration objects
        # :param duration: int (seconds)
        # :param genres: list of strings
        # :param release_date: not sure really
        # :param album: album object






