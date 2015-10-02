__author__ = 'Dani'

import time

from rdflib.namespace import RDF, FOAF

from wmera.graph_gen.rdflib.entities_gen.entity_to_triples import EntityToTriples
from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import *
from wmera.graph_gen.rdflib.index_utils.entity_counter_utils import increase_song_count
from wmera.graph_gen.rdflib.entities_gen.artist_to_triples import ArtistRawToTriplesUtils


class SongToTriples(EntityToTriples):
    def __init__(self, graph, ngram_repo, artist_to_triples, dataset_to_triples, entity_counter_repo, matcher):
        super(SongToTriples, self).__init__(graph, matcher)
        self._ngram_repo = ngram_repo
        self._artist_to_triples = artist_to_triples
        self._dataset_to_triples = dataset_to_triples
        self._entity_counter_repo = entity_counter_repo


    def add_song_triples_of_isolated_nodes_to_graph(self, song_parser):

        dataset_uri = self._dataset_to_triples.generate_dataset_uri(song_parser.dataset)

        # # Triples of the dataset object (source)
        for triple in DatasetToTriples.generate_dataset_triples(song_parser.dataset, dataset_uri):
            self._add_triple(triple)

        # Triples of the different songs
        counter = 0
        millis_tmp = int(round(time.time() * 1000))
        millis = 0
        total_mils = 0
        for song in song_parser.parse_songs():

            # ###################
            counter += 1  # ## TIME
            if counter % 1000 == 0:  # ## TIME
                millis = int(round(time.time() * 1000))  # ## TIME
                print counter, ",", millis - millis_tmp  # ## TIME
                total_mils += millis - millis_tmp  # ## TIME
                millis_tmp = millis  # ## TIME
            # ###################


            song_uri = self.generate_entity_uri(entity=song,
                                                alt_str=self.prepare_alt_str_for_song(song))
            is_new_song = True

            for triple in self._generate_needed_song_triples(song=song,
                                                             dataset_uri=dataset_uri,
                                                             song_uri=song_uri,
                                                             is_new_song=is_new_song,
                                                             isolated_song=True):
                self._add_triple(triple)
        print total_mils
        return self._graph

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
        for song in song_parser.parse_songs():

            # ###################
            counter += 1  # ## TIME
            if counter % 100 == 0:  # ## TIME
                millis = int(round(time.time() * 1000))  # ## TIME
                print counter, ",", millis - millis_tmp  # ## TIME
                total_mils += millis - millis_tmp  # ## TIME
                millis_tmp = millis  # ## TIME
            # ###################

            song_uri = self._get_existing_song_uri(song)
            is_new_song = False
            if song_uri is None:
                song_uri = self.generate_entity_uri(entity=song,
                                                    alt_str=self.prepare_alt_str_for_song(song))
                is_new_song = True

            for triple in self._generate_needed_song_triples(song=song,
                                                             dataset_uri=dataset_uri,
                                                             song_uri=song_uri,
                                                             is_new_song=is_new_song):
                self._add_triple(triple)
        print total_mils
        return self._graph


    def _generate_needed_song_triples(self, song, dataset_uri, song_uri, is_new_song, isolated_song=False):

        if is_new_song:
            for triple in self._generate_triples_for_new_song(song=song,
                                                              dataset_uri=dataset_uri,
                                                              isolated_song=isolated_song):
                yield triple
        else:
            for triple in self._generate_triples_for_existing_song(new_song=song,
                                                                   song_uri=song_uri,
                                                                   dataset_uri=dataset_uri,
                                                                   ngram_repo=self._ngram_repo):
                yield triple


    def _get_existing_song_uri(self, song, threshold=1.5):
        # TODO: we can probably aply list of artist here.
        artist_name = None if len(song._artists) == 0 else song._artists[0].canonical  # Best computational form...
        candidates = self._matcher.find_song(name=song.canonical, artists=[artist_name])  # List of MeraBaseResult
        if candidates is None or len(candidates) == 0:
            return None
        elif candidates[0].get_max_score() > threshold:
            return URIRef(candidates[0].uri)
        else:
            return None


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
        artist_uri = None
        for artist in song.artists:
            is_new_artist = False
            if not isolated_song:
                artist_uri = self._artist_to_triples.get_existing_artist_uri(artist=artist)
                is_new_artist = False
            else:
                artist_uri = None
            if artist_uri is None:
                artist_uri = self.generate_entity_uri(entity=artist,
                                                      alt_str=ArtistRawToTriplesUtils.prepare_alt_str_for_raw_artist(
                                                          artist))
                is_new_artist = True
            for triple in self._artist_to_triples. \
                    generate_needed_artist_of_unknown_type_triples(artist=artist,
                                                                   dataset_uri=dataset_uri,
                                                                   artist_uri=artist_uri,
                                                                   is_new_artist=is_new_artist):
                yield triple

            # # Linking artist and song
            yield (song_uri, FOAF.maker, artist_uri)


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

        # # Discogs elems
        if song.discogs_id is not None:
            for triple in SongToTriples._generate_discogs_id_triples(entity=song,
                                                                     entity_uri=song_uri):
                yield triple

        if song.discogs_index is not None:
            for triple in SongToTriples._generate_discogs_index_triples(entity=song,
                                                                        entity_uri=song_uri):
                yield triple

        ##USOS elems
        if song.usos_transaction_id is not None:
            for triple in SongToTriples._generate_usos_transaction_id(entity=song,
                                                                      entity_uri=song_uri):
                yield triple

        if song.usos_isrc is not None:
            for triple in SongToTriples._generate_usos_isrc(entity=song,
                                                            entity_uri=song_uri):
                yield triple

        increase_song_count(entity_counter_repo=self._entity_counter_repo)

        # TODO tHE NEXT ARE STILL NOT IMPLEMENTED:
        # :param collaborations: list of collaboration objects
        # :param duration: int (seconds)
        # :param genres: list of strings
        # :param release_date: not sure really
        # :param album: album object


    @staticmethod
    def _generate_alt_titles_triples_of_song(song, song_uri, dataset_uri, ngram_repo):
        count = 0
        for alt_title in song.alternative_titles:
            for triple in SongToTriples._generate_alt_title_triples(song_uri=song_uri,
                                                                    alt_title=alt_title,
                                                                    dataset_uri=dataset_uri,
                                                                    ngram_repo=ngram_repo,
                                                                    current_alt_titles=count):
                yield triple
            count += 1


    @staticmethod
    def prepare_alt_str_for_song(song):
        result = ""
        for artist in song.artists:
            result += "_" + SongToTriples.normalize_for_uri(artist.canonical)
        for genre in song.genres:
            result += "_" + SongToTriples.normalize_for_uri(genre[0])
        while len(result) > 0 and result[0] == "_":
            result = result[1:]
        return result


    def _generate_triples_for_existing_song(self, new_song, song_uri, dataset_uri, ngram_repo):
        old_song = self._graph.get_song_by_uri(uri=song_uri)
        set_old_forms = set(old_song.identifying_forms)
        # Update canonical to include this source
        for triple in self.update_canonical_to_include_source(entity_uri=song_uri,
                                                              dataset_uri=dataset_uri):
            yield triple

        # #####################
        # Canonical
        if new_song.canonical == old_song.canonical:
            pass  # We don't need to do anything
        elif new_song.canonical not in set_old_forms:
            for triple in self._generate_alt_title_triples_for_existing_song(song_uri=song_uri,
                                                                             song=old_song,
                                                                             dataset_uri=dataset_uri,
                                                                             alt_title=new_song.canonical):
                yield triple
        else:
            for triple in self._generate_updating_triples_for_existing_alt_title(song_uri=song_uri,
                                                                                 dataset_uri=dataset_uri,
                                                                                 alt_title=new_song.canonical):
                yield triple

        # #####################
        # Artists
        # # Triples of the artists
        for artist in new_song.artists:
            artist_uri = self._artist_to_triples.get_existing_artist_uri(artist=artist)
            is_new_artist = False
            if artist_uri is None:
                artist_uri = self.generate_entity_uri(entity=artist,
                                                      alt_str=ArtistRawToTriplesUtils.prepare_alt_str_for_raw_artist(
                                                          artist))
                is_new_artist = True
            for triple in self._artist_to_triples. \
                    generate_needed_artist_of_unknown_type_triples(artist=artist,
                                                                   dataset_uri=dataset_uri,
                                                                   artist_uri=artist_uri,
                                                                   is_new_artist=is_new_artist):
                yield triple
            # # Linking artist and song
            yield (song_uri, FOAF.maker, artist_uri)  # It may be repeated, but it does not matter.

        # ########################
        # Alt_titles
        for an_alt_title in new_song.alternative_titles:
            if an_alt_title == old_song.canonical:
                pass  # Nothing to do. Work already done.
            elif an_alt_title not in set_old_forms:
                for triple in self._generate_alt_title_triples_for_existing_song(song=old_song,
                                                                                 song_uri=song_uri,
                                                                                 dataset_uri=dataset_uri,
                                                                                 alt_title=an_alt_title):
                    yield triple

            else:
                for triple in self._generate_updating_triples_for_existing_alt_title(song_uri=song_uri,
                                                                                     dataset_uri=dataset_uri,
                                                                                     alt_title=new_song.canonical):
                    yield triple


        # ########################
        # Country
        if new_song.country != old_song.country:
            pass  # TODO: NOT NECESSARY AT THIS POINT
        else:
            pass  # TODO: NOT NECESSARY AT THIS POINT

        # # Discogs elems
        if new_song.discogs_index is not None:
            for triple in SongToTriples._generate_discogs_id_triples(entity=new_song,
                                                                     entity_uri=song_uri):
                yield triple

        if new_song.discogs_id is not None:
            for triple in SongToTriples._generate_discogs_index_triples(entity=new_song,
                                                                        entity_uri=song_uri):
                yield triple

        ##USOS elems
        if new_song.usos_transaction_id is not None:
            for triple in SongToTriples._generate_usos_transaction_id(entity=new_song,
                                                                      entity_uri=song_uri):
                yield triple

        if new_song.usos_isrc is not None:
            for triple in SongToTriples._generate_usos_isrc(entity=new_song,
                                                            entity_uri=song_uri):
                yield triple


        # TODO THE NEXT ARE STILL NOT IMPLEMENTED:
        # :param collaborations: list of collaboration objects
        # :param duration: int (seconds)
        # :param genres: list of strings
        # :param release_date: not sure really
        # :param album: album object


    def _generate_alt_title_triples_for_existing_song(self, song, song_uri, dataset_uri, alt_title):
        for triple in SongToTriples._generate_alt_title_triples(alt_title=alt_title,
                                                                song_uri=song_uri,
                                                                dataset_uri=dataset_uri,
                                                                ngram_repo=self._ngram_repo,
                                                                current_alt_titles=len(song._alt_titles)):  # =(
            yield triple


    @staticmethod
    def _generate_alt_title_triples(alt_title, song_uri, dataset_uri, ngram_repo, current_alt_titles):
        for triple in EntityToTriples.generate_str_labelled_triples_and_ngram_variations(entity_uri=song_uri,
                                                                                         primary_predicate=WPRO.alternative_title,
                                                                                         intermediary_entity_uri=
                                                                                         URIRef(song_uri + "/alt_title"
                                                                                                 + str(
                                                                                                                 current_alt_titles + 1)),
                                                                                         str_text=alt_title,
                                                                                         dataset_uri=dataset_uri,
                                                                                         ngram_repo=ngram_repo):
            yield triple

    def _generate_updating_triples_for_existing_alt_title(self, song_uri, dataset_uri, alt_title):
        secondary_entity_uri = self._graph.get_uri_of_intermediary_of_text(primary_entity_uri=song_uri,
                                                                           primary_property=WPRO.alternative_title,
                                                                           matching_text=alt_title)
        yield (URIRef(secondary_entity_uri), WPRO.source, dataset_uri)

