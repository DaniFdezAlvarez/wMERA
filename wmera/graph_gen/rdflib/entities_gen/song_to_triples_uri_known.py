from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples

__author__ = 'Dani'
import time


from wmera.graph_gen.rdflib.entities_gen.song_to_triples import SongToTriples


class SongToTriplesUriKnown(SongToTriples):
    def __init__(self, graph, ngram_repo, artist_to_triples, dataset_to_triples, entity_counter_repo, matcher):
        super(SongToTriplesUriKnown, self).__init__(graph, ngram_repo, artist_to_triples, dataset_to_triples,
                                                    entity_counter_repo, matcher)

    def add_song_triples_to_graph(self, song_parser):
        dataset_uri = self._dataset_to_triples.generate_dataset_uri(song_parser.dataset)

        # # Triples of the dataset object (source)
        for triple in DatasetToTriples.generate_dataset_triples(song_parser.dataset, dataset_uri):
            self._add_triple(triple)

        # Triples of the different songs
        counter = 0
        millis_tmp = int(round(time.time() * 1000))
        millis = 0
        total_mils = 0
        for song_tuple in song_parser.parse_songs():
            print "Mira una!"

            # ###################
            counter += 1  # ## TIME
            if counter % 100 == 0:  # ## TIME
                millis = int(round(time.time() * 1000))  # ## TIME
                print counter, ",", millis - millis_tmp  # ## TIME
                total_mils += millis - millis_tmp  # ## TIME
                millis_tmp = millis  # ## TIME
            # ###################

            song_uri = song_tuple[0]
            print "____________"
            for triple in self._generate_needed_song_triples(song=song_tuple[1],
                                                             dataset_uri=dataset_uri,
                                                             song_uri=song_uri,
                                                             is_new_song=False):
                self._add_triple(triple)
                print triple
            print "____________"
        print total_mils
        return self._graph