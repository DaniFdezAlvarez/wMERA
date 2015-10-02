from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples

__author__ = 'Dani'

from wmera.graph_gen.rdflib.entities_gen.artist_to_triples import ArtistToTriples

BUFFER_WRITING_SIZE = 5000


class ArtistToTriplesPersistingIndexUris(ArtistToTriples):

    def __init__(self, graph, ngram_repo, dataset_to_triples, entity_counter_repo,
                 matcher, file_path_dict, reset_file_path=False):
        super(ArtistToTriplesPersistingIndexUris, self).__init__(graph, ngram_repo, dataset_to_triples,
                                                                 entity_counter_repo, matcher)
        self._file_path_dict = file_path_dict
        if reset_file_path:
            self._reset_file_path()
        self._buffer = []


    def _reset_file_path(self):
        with open(self._file_path_dict, "w") as file_io:
            file_io.write("")


    def add_artists_triples_to_graph(self, artist_parser):
        dataset_uri = self._dataset_to_triples.generate_dataset_uri(artist_parser.dataset)

        # # Triples of the dataset object (source)
        for triple in DatasetToTriples.generate_dataset_triples(dataset=artist_parser.dataset,
                                                                dataset_uri=dataset_uri):
            self._add_triple(triple)

        # Triples of the different artists
        for artist in artist_parser.parse_artists():
            artist_uri = self.get_existing_artist_uri(artist)
            is_new_artist = False
            if artist_uri is None:
                artist_uri = self.generate_entity_uri(entity=artist, alt_str=self.prepare_alt_str_for_artist(artist))
                is_new_artist = True
            for triple in self.generate_needed_artist_of_unknown_type_triples(artist=artist,
                                                                              dataset_uri=dataset_uri,
                                                                              artist_uri=artist_uri,
                                                                              is_new_artist=is_new_artist):
                self._add_triple(triple)
            self._persist_uri_in_dict(artist.discogs_id, artist_uri)

        if len(self._buffer) != 0:
            self._persist_buffer()  # Persisting last URIS
        return self._graph


    def _persist_uri_in_dict(self, artist_discogs_id, artist_uri):
        self._buffer.append(str(artist_discogs_id) + "|" + artist_uri)
        if len(self._buffer) == BUFFER_WRITING_SIZE:
            self._persist_buffer()


    def _persist_buffer(self):
        with open(self._file_path_dict, "a") as file_io:
            for elem in self._buffer:
                file_io.write(elem + "\n")
        self._buffer = []

