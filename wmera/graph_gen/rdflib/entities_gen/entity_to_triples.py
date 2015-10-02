__author__ = 'Dani'

from rdflib.namespace import RDF, RDFS, FOAF
from rdflib import Literal

from wmera.mera_core.str_ops.normalization import normalize
from ..rdf_utils.namespaces_handler import *
from wmera.graph_gen.rdflib.index_utils.ngrams_utils import update_ngrams_of_entity


class EntityToTriples(object):
    """
    Abstract class.

    Private methods can be accessed from entities_gen classes. The protection should be
    similar to java's package

    """

    def __init__(self, graph, matcher):
        """
        :param graph: implementation of MeraGraph interface
        :param matcher: MeraMatcher object
        :return:
        """
        self._graph = graph
        self._matcher = matcher

    def _add_triple(self, triple):
        """
        Triple is expected to be a TUPLE with 3 items:
        pos0: subject
        pos1: predicate
        pos2: object

        :param triple: tuple of 3 items
        :return:
        """
        self._graph.add_triple(triple)


    def generate_entity_uri(self, entity, alt_str):
        """
        It returns a unique URI based on the entity info and the ones already contained in the graph.
        :param entity:
        :param alt_str:
        :return:
        """
        candidate_end = EntityToTriples.normalize_for_uri(entity.canonical)
        candidate_uri = went.term(candidate_end)
        if not self._already_exist_in_graph(candidate_uri):
            return candidate_uri
        alt_pieces = alt_str.split("_")
        for piece in alt_pieces:
            candidate_end += "_" + EntityToTriples.normalize_for_uri(piece)
            candidate_uri = went.term(candidate_end)
            if not self._already_exist_in_graph(candidate_uri):
                return candidate_uri

        i = 0
        candidate_end += "_"
        while self._already_exist_in_graph(went.term(candidate_end + str(i))):
            i += 1
        return went.term((candidate_end + str(i)))


    @staticmethod
    def generate_str_labelled_triples_and_ngram_variations(entity_uri, primary_predicate, intermediary_entity_uri,
                                                           str_text, dataset_uri, ngram_repo):
        """
        It yields the needed triples to link an entity representing a real object (artist, discogs,...) with a piece
         of information labelled with its source (its dataset) To do that, we are linking the real entity with
         an artificial one, that points to the piece of info and to the source.

         It also variates the apparitions of the test_ngrams stored in the ngram index, assuming that "str_text" shloud be
         splitted in test_ngrams and associated to "entity_URI"

        :param entity_uri: URI of the entity we that we want to add info about
        :param primary_predicate: predicate that shows the nature of the linked data with the entity_URI
        :param intermediary_entity_uri: URI of the intermediary URI that we use for link the final str with the source
        :param str_text: textual info to be linked
        :param dataset_uri: URI of the dataset that provides the info
        :param ngram_repo: repository object to use for updating the test_ngrams info
        :return: as many triples yielded as needed
        """

        for triple in EntityToTriples._generate_str_labelled_triples(entity_uri=entity_uri,
                                                                     primary_predicate=primary_predicate,
                                                                     intermediary_entity_uri=intermediary_entity_uri,
                                                                     str_text=str_text,
                                                                     dataset_uri=dataset_uri):
            yield triple

        update_ngrams_of_entity(entity_uri=entity_uri,
                                str_text=str_text,
                                repo=ngram_repo)

    @staticmethod
    def _generate_str_labelled_triples(entity_uri, primary_predicate, intermediary_entity_uri,
                                       str_text, dataset_uri):
        """
        It yields the needed triples to link an entity representing a real object (artist, discogs,...) with a piece
         of information labelled with its source (its dataset) To do that, we are linking the real entity with
         an artificial one, that points to the piece of info and to the source.


        :param entity_uri: URI of the entity we that we want to add info about
        :param primary_predicate: predicate that shows the nature of the linked data with the entity_URI
        :param intermediary_entity_uri: URI of the intermediary URI that we use for link the final str with the source
        :param str_text: textual info to be linked
        :param dataset_uri: URI of the dataset that provides the info

        :return: as many triples yielded as needed


        """
        yield (entity_uri, primary_predicate, intermediary_entity_uri)
        yield (intermediary_entity_uri, RDF.type, WTYP.str_labelled)
        yield (intermediary_entity_uri, RDFS.label, Literal(str_text))
        yield (intermediary_entity_uri, WPRO.source, dataset_uri)


    @staticmethod
    def _generate_entity_labelled_triples(entity_uri, primary_predicate, intermediary_entity_uri,
                                          target_entity_uri, dataset_uri):
        """
        It yields the needed triples to link an entity representing a real object (artist, discogs,...) with a entity
         labelled with the source (its dataset) that provides that relation. To do that, we are linking the first
         entity with an artificial one, that points to the target entity and to the source.

        :param entity_uri: URI of the entity we that we want to add info about
        :param primary_predicate: predicate that shows the nature of the linked data with the entity_URI
        :param intermediary_entity_uri: URI of the intermediary URI that we use for link the final str with the source
        :param target_entity_uri: entity that will be pointed (object) by the first one (subject)
        :param dataset_uri: URI of the dataset that provides the info
        :return: as many triples yielded as needed
        """
        yield (entity_uri, primary_predicate, intermediary_entity_uri)
        yield (intermediary_entity_uri, RDF.type, WTYP.str_labelled)
        yield (intermediary_entity_uri, WPRO.entity_target, target_entity_uri)
        yield (intermediary_entity_uri, WPRO.source, dataset_uri)


    @staticmethod
    def _generate_canonical_triples(entity, entity_uri, dataset_uri, ngram_repo):
        """
        All the entities has a canonical name, and that is why this method can (should) be here

        :param entity:
        :param entity_uri:
        :param dataset_uri:
        :return:
        """
        for triple in EntityToTriples. \
                generate_str_labelled_triples_and_ngram_variations(entity_uri=entity_uri,
                                                                   primary_predicate=FOAF.name,
                                                                   intermediary_entity_uri=EntityToTriples.
                                                                           generate_canonical_uri_prop(entity_uri),
                                                                   str_text=entity.canonical,
                                                                   dataset_uri=dataset_uri,
                                                                   ngram_repo=ngram_repo):
            yield triple

    @staticmethod
    def update_canonical_to_include_source(entity_uri, dataset_uri):
        for triple in EntityToTriples.\
                generate_updating_triples_to_attach_a_source_to_a_property(intermediate_entity_uri=EntityToTriples.
                                                                                generate_canonical_uri_prop(entity_uri),
                                                                           dataset_uri=dataset_uri):
            yield triple

    @staticmethod
    def generate_updating_triples_to_attach_a_source_to_a_property(intermediate_entity_uri, dataset_uri):
        yield (intermediate_entity_uri, WPRO.source, dataset_uri)

    @staticmethod
    def generate_canonical_uri_prop(entity_uri):
        return entity_uri + "/canonical"

    @staticmethod
    def _generate_country_triples(entity, entity_uri, dataset_uri):
        country_uri = EntityToTriples._get_country_uri(entity.country)
        if country_uri is not None:
            for triple in EntityToTriples \
                    ._generate_entity_labelled_triples(entity_uri=entity_uri,
                                                       primary_predicate=MO.origin,
                                                       intermediary_entity_uri=entity_uri + "/country",
                                                       target_entity_uri=country_uri,
                                                       dataset_uri=dataset_uri):
                yield triple

    @staticmethod
    def _generate_discogs_id_triples(entity, entity_uri):
        yield (entity_uri, WPRO.discogs_id, Literal(entity.discogs_id))

    @staticmethod
    def _generate_discogs_index_triples(entity, entity_uri):
        yield (entity_uri, WPRO.discogs_index, Literal(entity.discogs_index))

    @staticmethod
    def _generate_usos_transaction_id(entity, entity_uri):
        yield (entity_uri, WPRO.usos_transaction_id, Literal(entity.usos_transaction_id))

    @staticmethod
    def _generate_usos_isrc(entity, entity_uri):
        yield (entity_uri, WPRO.usos_isrc, Literal(entity.usos_isrc))


    def _already_exist_in_graph(self, candidate_uri):
        return self._graph.already_exist_in_graph(candidate_uri)


    @staticmethod
    def normalize_for_uri(original_str):
        # TODO fuera caracteres raros
        return normalize(original_str).replace(" ", "_")


    @staticmethod
    def _get_country_uri(str_country):
        # TODO: NOPE. MORE COMPLEX THAN THIS
        return went.term(EntityToTriples.normalize_for_uri(str_country))



