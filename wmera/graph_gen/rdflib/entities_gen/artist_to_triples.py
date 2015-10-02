__author__ = 'Dani'

from rdflib.namespace import RDF

from wmera.graph_gen.rdflib.entities_gen.entity_to_triples import EntityToTriples
from wmera.graph_gen.rdflib.entities_gen.dataset_to_triples import DatasetToTriples
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import *
from wmera.graph_gen.rdflib.index_utils.entity_counter_utils import increase_artist_count
from wmera.mera_core.model.entities import ArtistPerson, ArtistGroup


class ArtistToTriples(EntityToTriples):
    def __init__(self, graph, ngram_repo, dataset_to_triples, entity_counter_repo, matcher):
        super(ArtistToTriples, self).__init__(graph=graph, matcher=matcher)
        self._ngram_repo = ngram_repo
        self._dataset_to_triples = dataset_to_triples
        self._artist_person_gen = ArtistPersonToTriplesUtils(graph, ngram_repo, self)
        self._artist_raw_gen = ArtistRawToTriplesUtils(graph, ngram_repo, self)
        self._artist_group_gen = ArtistGroupToTriplesUtils(graph, ngram_repo, self)
        self._entity_counter_repo = entity_counter_repo


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

        return self._graph


    def generate_needed_artist_of_unknown_type_triples(self, artist, dataset_uri, artist_uri, is_new_artist):
        if isinstance(artist, ArtistPerson):
            for triple in self._artist_person_gen.generate_needed_artist_person_triples(artist=artist,
                                                                                        dataset_uri=dataset_uri,
                                                                                        artist_uri=artist_uri,
                                                                                        is_new_artist=is_new_artist):
                yield triple

        elif isinstance(artist, ArtistGroup):
            for triple in self._artist_group_gen.generate_needed_artist_group_triples(artist_group=artist,
                                                                                      artist_uri=artist_uri,
                                                                                      dataset_uri=dataset_uri,
                                                                                      is_new_artist=is_new_artist):
                yield triple
        else:
            for triple in self._artist_raw_gen.generate_needed_artist_raw_triples(artist=artist,
                                                                                  dataset_uri=dataset_uri,
                                                                                  artist_uri=artist_uri,
                                                                                  is_new_artist=is_new_artist):
                yield triple


    @staticmethod
    def _generate_alias_triples_for_artist(artist, artist_uri, dataset_uri, ngram_repo):
        count = 0
        for alias in artist.aliases:
            for triple in ArtistToTriples. \
                    _generate_alias_triples(artist_uri=artist_uri,
                                            alias=alias,
                                            dataset_uri=dataset_uri,
                                            ngram_repo=ngram_repo,
                                            current_aliases=count):
                yield triple
            count += 1

    @staticmethod
    def _generate_alias_triples(artist_uri, dataset_uri, ngram_repo, alias, current_aliases):
        for triple in EntityToTriples. \
                generate_str_labelled_triples_and_ngram_variations(entity_uri=artist_uri,
                                                                   primary_predicate=WPRO.alias,
                                                                   intermediary_entity_uri=URIRef(artist_uri + "/alias"
                                                                           + str(current_aliases + 1)),
                                                                   str_text=alias,
                                                                   dataset_uri=dataset_uri,
                                                                   ngram_repo=ngram_repo):
            yield triple


    def generate_namevar_triples_for_existing_artist(self, artist, artist_uri, namevar, dataset_uri, offset_namevars=0):
        for triple in ArtistToTriples._generate_namevar_triples(namevar=namevar,
                                                                artist_uri=artist_uri,
                                                                dataset_uri=dataset_uri,
                                                                ngram_repo=self._ngram_repo,
                                                                current_namevars=len(list(artist.namevars)) +
                                                                        offset_namevars):
            yield triple

    def generate_alias_triples_for_existing_artist(self, artist, artist_uri, alias, dataset_uri, offset_alias=0):
        for triple in ArtistToTriples._generate_alias_triples(alias=alias,
                                                              artist_uri=artist_uri,
                                                              dataset_uri=dataset_uri,
                                                              ngram_repo=self._ngram_repo,
                                                              current_aliases=len(list(artist.aliases)) +
                                                                      offset_alias):  # Awful...
            yield triple

    def generate_updating_triples_for_existing_namevar(self, artist_uri, namevar, dataset_uri):
        secondary_entity_uri = self._graph.get_uri_of_intermediary_of_text(primary_entity_uri=artist_uri,
                                                                           primary_property=WPRO.namevar,
                                                                           matching_text=namevar)
        yield (URIRef(secondary_entity_uri), WPRO.source, dataset_uri)

    def generate_updating_triples_for_existing_alias(self, artist_uri, alias, dataset_uri):
        secondary_entity_uri = self._graph.get_uri_of_intermediary_of_text(primary_entity_uri=artist_uri,
                                                                           primary_property=WPRO.alias,
                                                                           matching_text=alias)
        yield (URIRef(secondary_entity_uri), WPRO.source, dataset_uri)


    @staticmethod
    def _generate_namevars_triples_for_artist(artist, artist_uri, dataset_uri, ngram_repo):
        count = 0
        for namevar in artist.namevars:
            for triple in ArtistToTriples._generate_namevar_triples(namevar=namevar,
                                                                    artist_uri=artist_uri,
                                                                    dataset_uri=dataset_uri,
                                                                    ngram_repo=ngram_repo,
                                                                    current_namevars=count):
                yield triple
            count += 1

    @staticmethod
    def _generate_namevar_triples(namevar, artist_uri, dataset_uri, ngram_repo, current_namevars):
        for triple in EntityToTriples. \
                generate_str_labelled_triples_and_ngram_variations(entity_uri=artist_uri,
                                                                   primary_predicate=WPRO.namevar,
                                                                   intermediary_entity_uri=URIRef(
                                                                                           artist_uri + "/namevar" +
                                                                                   str(current_namevars + 1)),
                                                                   str_text=namevar,
                                                                   dataset_uri=dataset_uri,
                                                                   ngram_repo=ngram_repo):
            yield triple


    def get_existing_artist_uri(self, artist, threshold=0.95):
        """
        If the artist is already in the graph it returns its URI. If not, it return None
        :param artist:
        :return:
        """
        return None
        # candidates = self._matcher.find_artist(name=artist.canonical)  # Receiving a list of MeraBaseResult
        # if candidates is None or len(candidates) == 0:
        #     return None
        # elif candidates[0].get_max_score() > threshold:
        #     return URIRef(candidates[0].uri)
        # else:
        #     return None


    def generate_common_triples_for_new_artist_and_increase_count(self, artist, artist_uri, dataset_uri):
        """
        Different type or artist have a number of associated triples thar are built in the same way,
        accessing the same filed of the Artist superclass. And we build it here.

        Also, it calls methods to notify that there is a new artist in the graph, so the index
        must be updated.

        :param artist:
        :param artist_uri:
        :param dataset_uri:
        :return:
        """
        for triple in self.generate_common_triples_for_new_artist(artist=artist,
                                                                  artist_uri=artist_uri,
                                                                  dataset_uri=dataset_uri):
            yield triple
        increase_artist_count(self._entity_counter_repo)


    def generate_common_triples_for_existing_artist(self, artist_uri, old_artist, dataset_uri, new_artist,
                                                    function_to_update_existing_identifying_forms):
        set_old_forms = set()
        for form in old_artist.identifying_forms:
            set_old_forms.add(form)

        # Update canonical to include this source
        for triple in self.update_canonical_to_include_source(entity_uri=artist_uri,
                                                              dataset_uri=dataset_uri):
            yield triple

        # ######################
        # Canonical
        if new_artist.canonical == old_artist.canonical:
            pass
        elif new_artist.canonical not in set_old_forms:
            for triple in self.generate_namevar_triples_for_existing_artist(artist_uri=artist_uri,
                                                                            artist=old_artist,
                                                                            dataset_uri=dataset_uri,
                                                                            namevar=new_artist.canonical):
                yield triple
        else:
            for triple in self.generate_updating_triples_for_existing_namevar(artist_uri=artist_uri,
                                                                              dataset_uri=dataset_uri,
                                                                              namevar=new_artist.canonical):
                yield triple

        # Country
        if new_artist.country != old_artist.country:
            pass  # TODO: NOT NECESSARY AT THIS POINT
        else:
            pass  # TODO: NOT NECESSARY AT THIS POINT

        # Namevars
        namevars_count = 0
        for a_new_namevar in new_artist.namevars:
            if a_new_namevar not in set_old_forms:
                for triple in self.generate_namevar_triples_for_existing_artist(artist_uri=artist_uri,
                                                                                artist=old_artist,
                                                                                dataset_uri=dataset_uri,
                                                                                namevar=a_new_namevar,
                                                                                offset_namevars=namevars_count):
                    yield triple
                namevars_count += 1
            else:
                for triple in function_to_update_existing_identifying_forms(
                        form=a_new_namevar,
                        artist=old_artist,
                        artist_uri=artist_uri,
                        dataset_uri=dataset_uri):
                    yield triple

        # Aliases
        alias_count = 0
        for a_new_alias in new_artist.aliases:

            if a_new_alias not in set_old_forms:
                for triple in self.generate_alias_triples_for_existing_artist(artist_uri=artist_uri,
                                                                              artist=old_artist,
                                                                              dataset_uri=dataset_uri,
                                                                              alias=a_new_alias,
                                                                              offset_alias=alias_count):
                    yield triple
                alias_count += 1
            else:
                for triple in function_to_update_existing_identifying_forms(
                        form=a_new_alias,
                        artist=old_artist,
                        artist_uri=artist_uri,
                        dataset_uri=dataset_uri):
                    yield triple


    def generate_common_triples_for_new_artist(self, artist, artist_uri, dataset_uri):
        """
        Different type or artist have a number of associated triples thar are built in the same way,
        accessing the same filed of the Artist superclass. And we build it here.

        :param artist:
        :param artist_uri:
        :param dataset_uri:
        :return:
        :param artist:
        :param artist_uri:
        :param dataset_uri:
        :return:
        """

        for triple in ArtistToTriples._generate_canonical_triples(entity=artist,
                                                                  entity_uri=artist_uri,
                                                                  dataset_uri=dataset_uri,
                                                                  ngram_repo=self._ngram_repo):  # canonical
            yield triple


        # There wont be triples if there are not alias
        for triple in ArtistToTriples._generate_alias_triples_for_artist(artist=artist,
                                                                         artist_uri=artist_uri,
                                                                         dataset_uri=dataset_uri,
                                                                         ngram_repo=self._ngram_repo):  # alias
            yield triple

        # There wont be triples if there are not alias
        for triple in ArtistToTriples._generate_namevars_triples_for_artist(artist=artist,
                                                                            artist_uri=artist_uri,
                                                                            dataset_uri=dataset_uri,
                                                                            ngram_repo=self._ngram_repo):  # namevars
            yield triple

        if artist.country is not None:
            for triple in ArtistToTriples._generate_country_triples(entity=artist,
                                                                    entity_uri=artist_uri,
                                                                    dataset_uri=dataset_uri):  # country
                yield triple

    @staticmethod
    def prepare_alt_str_for_artist(artist):
        if isinstance(artist, ArtistPerson):
            return ArtistPersonToTriplesUtils.prepare_alt_str_for_artist_person(artist)
        elif isinstance(artist, ArtistGroupToTriplesUtils):
            return ArtistGroupToTriplesUtils.prepare_alt_str_for_group_artist(artist)
        else:
            return ArtistRawToTriplesUtils.prepare_alt_str_for_raw_artist(artist)


class ArtistRawToTriplesUtils(object):
    def __init__(self, graph, ngram_repo, artist_to_triples):
        self._graph = graph
        self._ngram_repo = ngram_repo
        self._artist_to_triples = artist_to_triples


    def generate_needed_artist_raw_triples(self, artist, dataset_uri, artist_uri, is_new_artist):

        if is_new_artist:
            for triple in self._generate_triples_for_new_raw_artist(artist=artist,
                                                                    artist_uri=artist_uri,
                                                                    dataset_uri=dataset_uri):
                yield triple
        else:
            for triple in self._generate_triples_for_existing_raw_artist(artist=artist,
                                                                         artist_uri=artist_uri,
                                                                         dataset_uri=dataset_uri):
                yield triple

    def _generate_triples_for_new_raw_artist(self, artist, artist_uri, dataset_uri):

        # Most approximated type using MO... todo revise
        yield (artist_uri, RDF.type, MO.music_artist)  # # triple ot type

        for triple in self._artist_to_triples.generate_common_triples_for_new_artist_and_increase_count(
                artist=artist,
                artist_uri=artist_uri,
                dataset_uri=dataset_uri):
            yield triple


    def _generate_triples_for_existing_raw_artist(self, artist, artist_uri, dataset_uri):
        old_artist = self._graph.get_artist_by_uri(artist_uri)
        for triple in self._artist_to_triples. \
                generate_common_triples_for_existing_artist(artist_uri=artist_uri,
                                                            new_artist=artist,
                                                            old_artist=old_artist,
                                                            dataset_uri=dataset_uri,
                                                            function_to_update_existing_identifying_forms=
                                                            self._generate_updating_triples_for_existing_identifying_form_of_raw_artist):
            yield triple


    def _generate_updating_triples_for_existing_identifying_form_of_raw_artist(self, form, artist,
                                                                               artist_uri, dataset_uri):
        if form == artist.canonical:
            pass  # Nothing to do. Canonical has already been updated

        else:
            success = False
            for a_namevar in artist.namevars:
                if a_namevar == form:
                    for triple in self._artist_to_triples. \
                            generate_updating_triples_for_existing_namevar(artist_uri=artist_uri,
                                                                           namevar=form,
                                                                           dataset_uri=dataset_uri):
                        yield triple
                    success = True
                    break
            if not success:
                for an_alias in artist.aliases:
                    if an_alias == form:
                        for triple in self._artist_to_triples. \
                                generate_updating_triples_for_existing_alias(artist_uri=artist_uri,
                                                                             alias=form,
                                                                             dataset_uri=dataset_uri):
                            yield triple
                    break


    @staticmethod
    def prepare_alt_str_for_raw_artist(artist):
        result = ""
        if artist.country is not None:
            result += EntityToTriples.normalize_for_uri(artist.country)
        return result


class ArtistPersonToTriplesUtils(object):
    def __init__(self, graph, ngram_repo, artist_to_triples):
        self._graph = graph
        self._ngram_repo = ngram_repo
        self._artist_to_triples = artist_to_triples

    def generate_needed_artist_person_triples(self, artist, dataset_uri, artist_uri, is_new_artist):
        if is_new_artist:
            for triple in self. \
                    _generate_triples_for_new_artist_person(artist_person=artist,
                                                            artist_uri=artist_uri,
                                                            dataset_uri=dataset_uri):
                yield triple
        else:
            for triple in self. \
                    _generate_triples_for_existing_artist_person(new_artist=artist,
                                                                 artist_uri=artist_uri,
                                                                 dataset_uri=dataset_uri):
                yield triple


    def _generate_triples_for_new_artist_person(self, artist_person, artist_uri, dataset_uri):
        yield (artist_uri, RDF.type, MO.music_artist)  # # triple ot type

        for triple in self._artist_to_triples.generate_common_triples_for_new_artist_and_increase_count(
                artist=artist_person,
                artist_uri=artist_uri,
                dataset_uri=dataset_uri):
            yield triple

        if artist_person.civil is not None:
            for triple in self._generate_civil_triples_for_artist(artist=artist_person,
                                                                  artist_uri=artist_uri,
                                                                  dataset_uri=dataset_uri):  # civil
                yield triple


    def _generate_civil_triples_for_artist(self, artist, artist_uri, dataset_uri):
        if artist.civil is not None:
            for triple in ArtistPersonToTriplesUtils._generate_civil_triples(artist_uri=artist_uri,
                                                                             dataset_uri=dataset_uri,
                                                                             civil_name_str=artist.civil,
                                                                             ngram_repo=self._ngram_repo):
                yield triple

    @staticmethod
    def _generate_civil_triples(artist_uri, dataset_uri, civil_name_str, ngram_repo):
        for triple in EntityToTriples. \
                generate_str_labelled_triples_and_ngram_variations(entity_uri=artist_uri,
                                                                   primary_predicate=WPRO.civil_name,
                                                                   intermediary_entity_uri=URIRef(
                                                                                   artist_uri + "/civil"),
                                                                   str_text=civil_name_str,
                                                                   dataset_uri=dataset_uri,
                                                                   ngram_repo=ngram_repo):
            yield triple

    def _generate_updating_triples_for_existing_civil(self, artist_uri, dataset_uri, civil_name):
        secondary_entity_uri = self._graph.get_uri_of_intermediary_of_text(primary_entity_uri=artist_uri,
                                                                           primary_property=WPRO.civil_name,
                                                                           matching_text=civil_name)
        yield (secondary_entity_uri, WPRO.source, dataset_uri)

    def _generate_triples_for_existing_artist_person(self, new_artist, artist_uri, dataset_uri):

        old_artist = self._graph.get_artist_person_by_uri(artist_uri)
        for triple in self._artist_to_triples. \
                generate_common_triples_for_existing_artist(new_artist=new_artist,
                                                            old_artist=old_artist,
                                                            artist_uri=artist_uri,
                                                            dataset_uri=dataset_uri,
                                                            function_to_update_existing_identifying_forms=
                                                            self._generate_updating_triples_for_existing_identifying_form_of_artist_person):
            yield triple

        # ######################
        # Civil
        if new_artist.civil is not None:
            if old_artist.civil is None:  # If the old artist hasn't got civil name
                for triple in ArtistPersonToTriplesUtils._generate_civil_triples(artist_uri=artist_uri,
                                                                                 dataset_uri=dataset_uri,
                                                                                 civil_name_str=new_artist.civil,
                                                                                 ngram_repo=self._ngram_repo):
                    yield triple
            elif old_artist.civil == new_artist.civil:  # If the new civil and the old one are the same.
                for triple in self._generate_updating_triples_for_existing_civil(artist_uri=artist_uri,
                                                                                 dataset_uri=dataset_uri,
                                                                                 civil_name=new_artist.canonical):
                    yield triple
            else:  # A different civil. Let's introduce it in the graph as a namevar
                for triple in self._artist_to_triples. \
                        generate_updating_triples_for_existing_namevar(artist_uri=artist_uri,
                                                                       dataset_uri=dataset_uri,
                                                                       namevar=new_artist.civil):
                    yield triple


    def _generate_updating_triples_for_existing_identifying_form_of_artist_person(self, form, artist,
                                                                                  artist_uri, dataset_uri):
        if form == artist.canonical:
            pass  # Nothing to do. Canonical has already been updated
        elif form == artist.civil:
            for triple in self._generate_updating_triples_for_existing_civil(artist_uri=artist_uri,
                                                                             dataset_uri=dataset_uri,
                                                                             civil_name=form):
                yield triple
        else:
            success = False
            for a_namevar in artist.namevars:
                if a_namevar == form:
                    for triple in self._artist_to_triples. \
                            generate_updating_triples_for_existing_namevar(artist_uri=artist_uri,
                                                                           namevar=form,
                                                                           dataset_uri=dataset_uri):
                        yield triple
                    success = True
                    break
            if not success:
                for an_alias in artist.aliases:
                    if an_alias == form:
                        for triple in self._artist_to_triples. \
                                generate_updating_triples_for_existing_alias(artist_uri=artist_uri,
                                                                             alias=form,
                                                                             dataset_uri=dataset_uri):
                            yield triple
                    break

    @staticmethod
    def prepare_alt_str_for_artist_person(artist):
        result = ""
        if artist.country is not None:
            result += ArtistToTriples.normalize_for_uri(artist.country)
        if artist.civil is not None:
            result += "_" + ArtistToTriples.normalize_for_uri(artist.civil)
        while len(result) > 0 and result[0] == "_":
            result = result[1:]
        return result


class ArtistGroupToTriplesUtils(object):
    """
    Class containing methods to generate triples form an entity group

    """

    def __init__(self, graph, ngram_repo, artist_to_triples):
        self._graph = graph
        self._ngram_repo = ngram_repo
        self._artist_to_triples = artist_to_triples


    def generate_needed_artist_group_triples(self, artist_group, dataset_uri, artist_uri, is_new_artist):
        if is_new_artist:
            for triple in self. \
                    _generate_triples_for_new_artist_group(artist_group=artist_group,
                                                           artist_group_uri=artist_uri,
                                                           dataset_uri=dataset_uri):
                yield triple
        else:
            for triple in self. \
                    _generate_triples_for_existing_artist_group(artist_group=artist_group,
                                                                artist_uri=artist_uri,
                                                                dataset_uri=dataset_uri):
                yield triple


    def _generate_triples_for_new_artist_group(self, artist_group, artist_group_uri, dataset_uri):

        yield (artist_group_uri, RDF.type, MO.music_group)  # # triple of type

        # #Common artist triples
        for triple in self._artist_to_triples.generate_common_triples_for_new_artist_and_increase_count(
                artist_uri=artist_group_uri,
                artist=artist_group,
                dataset_uri=dataset_uri):
            yield triple

        # #triples for each member
        for artist_member in artist_group.members:
            member_uri = self._artist_to_triples.get_existing_artist_uri(artist=artist_member)
            is_new_artist = False
            if member_uri is None:
                member_uri = self._artist_to_triples.generate_entity_uri(entity=artist_member,
                                                                         alt_str=ArtistToTriples.
                                                                         prepare_alt_str_for_artist(artist_member))
                is_new_artist = True

            for triple in self._artist_to_triples. \
                    generate_needed_artist_of_unknown_type_triples(artist=artist_member,
                                                                   dataset_uri=dataset_uri,
                                                                   artist_uri=member_uri,
                                                                   is_new_artist=is_new_artist):
                yield triple
            yield (artist_group_uri, MO.member, member_uri)  # # triple linking with the member


    def _generate_triples_for_existing_artist_group(self, artist_group, artist_uri, dataset_uri):

        old_artist = self._graph.get_artist_person_by_uri(artist_uri)
        for triple in self._artist_to_triples. \
                generate_common_triples_for_existing_artist(new_artist=artist_group,
                                                            old_artist=old_artist,
                                                            artist_uri=artist_uri,
                                                            dataset_uri=dataset_uri,
                                                            function_to_update_existing_identifying_forms=
                                                            self._generate_updating_triples_for_existing_identifying_form_of_artist_group):
            yield triple

        # ######################
        # Members

        for artist_member in artist_group.members:
            member_uri = self._artist_to_triples.get_existing_artist_uri(artist=artist_member)
            is_new_artist = False
            if member_uri is None:
                member_uri = self._artist_to_triples.generate_entity_uri(entity=artist_member,
                                                                         alt_str=ArtistToTriples.
                                                                         prepare_alt_str_for_artist(artist_member))
                is_new_artist = True
                yield (artist_uri, MO.member, member_uri)  # triple linking with the new member
            else:
                if (artist_uri, MO.member, member_uri) not in self._graph:
                    yield (artist_uri, MO.member, member_uri)  # triple linking with the member,
                    # in case it was not already linked

            for triple in self._artist_to_triples. \
                    generate_needed_artist_of_unknown_type_triples(artist=artist_member,
                                                                   dataset_uri=dataset_uri,
                                                                   artist_uri=member_uri,
                                                                   is_new_artist=is_new_artist):
                yield triple


    def _generate_updating_triples_for_existing_identifying_form_of_artist_group(self, form, artist,
                                                                                 artist_uri, dataset_uri):
        if form == artist.canonical:
            pass  # Nothing to do. Canonical has already been updated

        else:
            success = False
            for a_namevar in artist.namevars:
                if a_namevar == form:
                    for triple in self._artist_to_triples. \
                            generate_updating_triples_for_existing_namevar(artist_uri=artist_uri,
                                                                           namevar=form,
                                                                           dataset_uri=dataset_uri):
                        yield triple
                    success = True
                    break
            if not success:
                for an_alias in artist.aliases:
                    if an_alias == form:
                        for triple in self._artist_to_triples. \
                                generate_updating_triples_for_existing_alias(artist_uri=artist_uri,
                                                                             alias=form,
                                                                             dataset_uri=dataset_uri):
                            yield triple
                    break


    @staticmethod
    def prepare_alt_str_for_group_artist(group_artist):
        return ArtistRawToTriplesUtils.prepare_alt_str_for_raw_artist(group_artist)