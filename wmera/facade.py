__author__ = 'Dani'

from wmera.query_gen.query_generator_cwr import CWRQueryGenerator
from wmera.mera_core.model.entities import Dataset


def json_matcher(json_cwr, executer_obj):
    query_gen = CWRQueryGenerator(str_json_content=json_cwr,
                                  config_path="Doesntmatteryet")

    return executer_obj.execute_queries_from_json(json_content=query_gen.gen_mera_json())


def json_enricher(json_matches, executer_obj, title_dataset, description=None,
                  download_link=None, home_page=None, date=None, serialization_path=None):
    """

    :param json_matches: json content (str) with the same format of the json results reveived when  json_matcher is
        invoked, but just containing those results that should be introduced in the graph
    :param executer_obj:
    :param title_dataset: Short name of the source from which the nwe data has been obtained
    :param description: OPTIONAL. Long description of the data source
    :param download_link: OPTIONAL. Link to download the data source
    :param home_page: OPTIONAL. Home page of the data source
    :param date: OPTIONAL. Date in which the data source has been computed
    :param serialization_path: if this param is not None, the grpah obtained at the end of the enrichment process
     will be serialized in the indicated path in turtle format
    :return:
    """
    executer_obj.introduce_json_matches_in_graph(json_matches_str=json_matches,
                                                 dataset_obj=Dataset(title=title_dataset,
                                                                     description=description,
                                                                     download_link=download_link,
                                                                     home_page=home_page,
                                                                     date=date),
                                                 serialization_path=serialization_path)

