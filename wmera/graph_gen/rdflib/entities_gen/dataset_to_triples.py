__author__ = 'Dani'

from rdflib.namespace import RDF, RDFS
from rdflib import Literal

from wmera.graph_gen.rdflib.entities_gen.entity_to_triples import EntityToTriples
from ..rdf_utils.namespaces_handler import *


class DatasetToTriples(EntityToTriples):
    """
    Methods should be accessed from entities_gen classes. The protection should be
    similar to java's package

    """

    def __init__(self, graph, matcher):
        super(DatasetToTriples, self).__init__(graph, matcher)

    @staticmethod
    def generate_dataset_triples(dataset, dataset_uri):
        yield (dataset_uri, RDF.type, wtyp.source)
        yield (dataset_uri, DC.title, Literal(dataset.title))
        if dataset.description is not None:
            yield (went.term(dataset_uri), RDFS.label, Literal(dataset.description))
        if dataset.download_link is not None:
            yield (went.term(dataset_uri), WPRO.download_link, Literal(dataset.download_link))
        if dataset.home_page is not None:
            yield (went.term(dataset_uri), WPRO.home_page, Literal(dataset.home_page))
        if dataset.date is not None:
            pass  # TODO: i don't care at this moment about this.


    def generate_dataset_uri(self, dataset):
        """
        It return a unique URI based on the content of the dataset object and the URIs already
        contained in the graph
        :return:
        """
        candidate_end = EntityToTriples.normalize_for_uri(dataset.title)
        if dataset.date is not None:
            candidate_end += "_" + dataset.date.replace("-", "_")
        candidate_uri = went.term(candidate_end)
        index = 97  # 97 is the ASCII number equivalent of char "a"
        while self._already_exist_in_graph(candidate_uri):
            candidate_uri = went.term(candidate_end + "_" + chr(index))
            index += 1
        return candidate_uri
