__author__ = 'Dani'

from wmera.mera_core.mera_graph.mera_graph_interface import MeraGraphInterface
from wmera.graph_gen.rdflib.rdf_utils.queries import Queries
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import *
from rdflib import Graph

from wmera.mera_core.labelled_model.entities import *


class MeraRdflibGraph(MeraGraphInterface):
    def __init__(self, rdflib_graph=None):
        self._graph = rdflib_graph
        if rdflib_graph is None:
            self._graph = Graph()

        bind_namespaces(self._graph)


    def __contains__(self, triple):
        return triple in self._graph

    def add_triple(self, triple):
        if triple[0] is None or triple[1] is None or triple[2] is None:
            print triple
        self._graph.add(triple)

    def already_exist_in_graph(self, uri):
        return self._graph.__contains__((uri, None, None))

    def serialize(self, out_format='turtle'):
        return self._graph.serialize(format=out_format)


    def get_artist_of_unknown_type_by_uri(self, uri):
        rows_canonical = self._graph.query(Queries.find_canonical_compiled(uri))
        canonical_tuple = MeraRdflibGraph._get_double_rows_simple_result(rows_canonical)
        if canonical_tuple is None:
            return None

        rows_aliases = self._graph.query(Queries.find_aliases_compiled(uri))
        rows_namevars = self._graph.query(Queries.find_namevars_compiled(uri))
        rows_country = self._graph.query(Queries.find_country_compiled(uri))
        rows_civil = self._graph.query(Queries.find_civil_compiled(uri))

        if rows_civil is not None:  # It is an ArtistPerson
            return MeraArtistPerson(labelled_canonical=canonical_tuple,
                                    labelled_aliases=MeraRdflibGraph._get_double_rows_multiple_result(rows_aliases),
                                    labelled_namevars=MeraRdflibGraph._get_double_rows_multiple_result(rows_namevars),
                                    labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country),
                                    labelled_civil=MeraRdflibGraph._get_double_rows_simple_result(rows_civil))
        rows_members = self._graph.query(Queries.find_members_uri_compiled(uri))
        if rows_members is None:  # It has not members, so it hasn't group properties
            return MeraArtist(labelled_canonical=canonical_tuple,
                              labelled_aliases=MeraRdflibGraph._get_double_rows_multiple_result(rows_aliases),
                              labelled_namevars=MeraRdflibGraph._get_double_rows_multiple_result(rows_namevars),
                              labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country))
        # By elimination, it is a group
        object_members = None
        uri_members = MeraRdflibGraph._get_single_rows_multiple_result(rows_members)
        if uri_members is not None:
            object_members = [self.get_artist_person_by_uri(person) for person in uri_members]

        return MeraArtistGroup(labelled_canonical=canonical_tuple,
                               labelled_aliases=MeraRdflibGraph._get_double_rows_multiple_result(rows_aliases),
                               labelled_namevars=MeraRdflibGraph._get_double_rows_multiple_result(rows_namevars),
                               labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country),
                               members=object_members)


    def get_artist_by_uri(self, uri):
        rows_canonical = self._graph.query(Queries.find_canonical_compiled(uri))
        canonical_tuple = MeraRdflibGraph._get_double_rows_simple_result(rows_canonical)
        if canonical_tuple is None:
            return None

        rows_aliases = self._graph.query(Queries.find_aliases_compiled(uri))
        rows_namevars = self._graph.query(Queries.find_namevars_compiled(uri))
        rows_country = self._graph.query(Queries.find_country_compiled(uri))

        return MeraArtist(labelled_canonical=canonical_tuple,
                          labelled_aliases=MeraRdflibGraph._get_double_rows_multiple_result(rows_aliases),
                          labelled_namevars=MeraRdflibGraph._get_double_rows_multiple_result(rows_namevars),
                          labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country))


    def get_artist_person_by_uri(self, uri):
        rows_canonical = self._graph.query(Queries.find_canonical_compiled(uri))
        canonical_tuple = MeraRdflibGraph._get_double_rows_simple_result(rows_canonical)
        if canonical_tuple is None:
            return None

        rows_aliases = self._graph.query(Queries.find_aliases_compiled(uri))
        rows_namevars = self._graph.query(Queries.find_namevars_compiled(uri))
        rows_country = self._graph.query(Queries.find_country_compiled(uri))
        rows_civil = self._graph.query(Queries.find_civil_compiled(uri))

        return MeraArtistPerson(labelled_canonical=canonical_tuple,
                                labelled_aliases=MeraRdflibGraph._get_double_rows_multiple_result(rows_aliases),
                                labelled_namevars=MeraRdflibGraph._get_double_rows_multiple_result(rows_namevars),
                                labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country),
                                labelled_civil=MeraRdflibGraph._get_double_rows_simple_result(rows_civil))


    def get_artist_group_by_uri(self, uri):
        rows_canonical = self._graph.query(Queries.find_canonical_compiled(uri))
        canonical_tuple = MeraRdflibGraph._get_double_rows_simple_result(rows_canonical)
        if canonical_tuple is None:
            return None

        rows_aliases = self._graph.query(Queries.find_aliases_compiled(uri))
        rows_namevars = self._graph.query(Queries.find_namevars_compiled(uri))
        rows_country = self._graph.query(Queries.find_country_compiled(uri))
        rows_members = self._graph.query(Queries.find_members_uri_compiled(uri))

        object_members = None
        uri_members = MeraRdflibGraph._get_single_rows_multiple_result(rows_members)
        if uri_members is not None:
            object_members = [self.get_artist_person_by_uri(person) for person in uri_members]

        return MeraArtistGroup(labelled_canonical=canonical_tuple,
                               labelled_aliases=MeraRdflibGraph._get_double_rows_multiple_result(rows_aliases),
                               labelled_namevars=MeraRdflibGraph._get_double_rows_multiple_result(rows_namevars),
                               labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country),
                               members=object_members)


    def get_song_by_uri(self, uri):
        rows_canonical = self._graph.query(Queries.find_canonical_compiled(uri))
        canonical_tuple = MeraRdflibGraph._get_double_rows_simple_result(rows_canonical)
        if canonical_tuple is None:
            return None
        # rows_artist = self._graph.query(Queries.find_artists_uri_compiled(uri))
        rows_compilers = self._graph.query(Queries.find_compiler_uri_compiled(uri))
        rows_genres = self._graph.query(Queries.find_genres_compiled(uri))
        rows_alt_titles = self._graph.query(Queries.find_alternative_titles_compiled(uri))
        # rows_country = self._graph.query(Queries.find_country_compiled(uri))
        rows_discogs_id = self._graph.query(Queries.find_discogs_id_compiled(uri))
        rows_discogs_index = self._graph.query(Queries.find_discogs_index_compiled(uri))
        rows_transaction_id = self._graph.query(Queries.find_usos_transaction_id_compiled(uri))
        rows_isrc = self._graph.query(Queries.find_usos_isrc_compiled(uri))

        # rows_duration = None  # Not used yet
        # rows_date = None  # Not used yet
        # rows_album = None  # Not used yet


        return MeraSong(labelled_canonical=canonical_tuple,
                        labelled_alt_titles=MeraRdflibGraph._get_double_rows_multiple_result(rows_alt_titles),
                        labelled_collaborations=self._build_labelled_collaborations_from_rows(rows_compilers,
                                                                                              ROLE_WRITER),
                        # labelled_country=MeraRdflibGraph._get_double_rows_simple_result(rows_country),
                        # artists=MeraRdflibGraph._get_single_rows_multiple_result(rows_artist),
                        duration=None,
                        labelled_genres=MeraRdflibGraph._get_double_rows_multiple_result(rows_genres),
                        release_date=None,
                        album=None,
                        discogs_index=MeraRdflibGraph._get_single_rows_simple_result(rows_discogs_index),
                        discogs_id=MeraRdflibGraph._get_single_rows_simple_result(rows_discogs_id),
                        usos_transaction_id=MeraRdflibGraph._get_single_rows_simple_result(rows_transaction_id),
                        usos_isrc=MeraRdflibGraph._get_single_rows_simple_result(rows_isrc))

    def get_uri_of_intermediary_of_text(self, primary_entity_uri, primary_property, matching_text):
        rows_intermediary_uri = self._graph.query(
            Queries.find_intermediary_uri_for_text_compiled(primary_property=primary_property,
                                                            primary_entity_uri=primary_entity_uri,
                                                            matching_text=matching_text))
        return self._get_single_rows_simple_result(rows_intermediary_uri)

    def get_uri_of_intermediary_of_entity(self, primary_entity_uri, primary_property, target_entity):
        rows_intermediary_uri = self._graph.query(
            Queries.find_intermediary_uri_for_target_entity_compiled(primary_entity_uri=primary_entity_uri,
                                                                     primary_property=primary_property,
                                                                     entity_target_uri=target_entity)
        )
        return self._get_single_rows_simple_result(rows_intermediary_uri)

    def get_songs_of_artist(self, uri):
        # TODO
        pass

    def get_artists_and_collaborators_of_song_by_uri(self, uri):
        rows_artists = self._graph.query(Queries.find_artists_uri_compiled(uri))
        rows_compilers = self._graph.query(Queries.find_compiler_uri_compiled(uri))

        artist_uris = self._get_single_rows_multiple_result(rows_artists)
        if artist_uris is not None:
            for artist_uri in artist_uris:
                yield self.get_artist_by_uri(artist_uri)

        compilers_tuples = self._get_double_rows_multiple_result(rows_compilers)
        if compilers_tuples is not None:
            for compiler_tuple in compilers_tuples:
                yield self.get_artist_by_uri(compiler_tuple[0])


    def _build_labelled_collaborations_from_rows(self, rows, role):
        """
        It returns collaborations labbeled (tuples of two positions, being the first one
        a collaboration object and the second one the uri of a source.
        :param rows:
        :param role:
        :return:
        """
        possible_collaborations = MeraRdflibGraph._get_double_rows_multiple_result(rows)
        if possible_collaborations is not None:
            for a_collaboration in possible_collaborations:
                yield (Collaboration(collaborator=self.get_artist_by_uri(a_collaboration[0]),
                                     role=role), a_collaboration[1])
        else:
            pass  # Yield No elements


    @staticmethod
    def _get_double_rows_simple_result(rows):
        """
        It expects a list of tuples of two positions,
        where the first pos is some kind of data
        and the second one is the URI of a source

        It also assumes that the first pos of every tuple
        should be always equal. Only the uri of the source
        may change in case of having more than one tuple

        It returns a tuple in which the first pos is
        the first data of every rows and the second one a
        list with all the sources (even if there are a single
        source)

        If rows is None or len(rows) == 0, the returns None

        :param rows:
        :return:
        """
        if rows is None or len(rows) == 0:
            return None
        tuple_0 = []  # It is expected to be the same str across all the tuples
        tuple_1 = []
        for row in rows:
            tuple_0.append(str(row[0].encode("utf-8")))
            tuple_1.append(str(row[1].encode("utf-8")))

        return tuple_0[0], tuple_1

    @staticmethod
    def _get_double_rows_multiple_result(rows):
        """
        It expects a list of tuples of two positions,
        where the first pos is some kind of data (str)
        and the second one is the URI of a source

        The data of the first pos and the source of the second
        one could be repeated.

        It returns a list of tuples, where the first element
        of each one is one of the data found in the rows and the second
        one a list containing all the sources in which the first element
        appeared (the first element is never repeated).

        If rows is None or len(rows) == 0, the returns None

        :param rows:
        :return:
        """
        if rows is None or len(rows) == 0:
            return None
        tmp_dict = {}
        for row in rows:
            if str(row[0].encode("utf-8")) not in tmp_dict:
                tmp_dict[str(row[0].encode("utf-8"))] = []
            tmp_dict[str(row[0].encode("utf-8"))].append(str(row[1].encode("utf-8")))
        return tmp_dict.items()

    @staticmethod
    def _get_single_rows_simple_result(rows):
        """
        It expects to receive a list of rows containing just
        one element, which is a tuple of a single position.

        It returns the contained string in case of receiving that
        and None in case rows == None or len(rows)==0
        :param rows:
        :return:
        """
        if rows is None or len(rows) == 0:
            return None

        for row in rows:  # Strange, but only one element expected. Maybe a check could be fine
            return str(row[0].encode("utf-8"))


    @staticmethod
    def _get_single_rows_multiple_result(rows):
        """
        It expects to receive a list of tuples of a single element

        If rows is None or len(rows) == 0, it returns None.
        Else, it return a list of the string found in the tuples.
        It is assuming that those strings appear only once in the
        list.

        :param rows:
        :return:
        """
        if rows is None or len(rows) == 0:
            return None
        result = []
        for row in rows:
            result.append(str(row[0].encode("utf-8")))
        return result
