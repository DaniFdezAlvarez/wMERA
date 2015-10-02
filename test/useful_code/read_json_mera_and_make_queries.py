__author__ = 'Dani'

from wmera.controller.query_executer import QueryExecuter
from test.t_utils.t_factory import get_mera_matcher_with_data, get_empty_mera_matcher
from wmera.mera_core.result.formater_interface import MeraFormaterInterface
from wmera.utils import rel_path_to_file
from wmera.controller.formater_to_json import FormaterToJson
from wmera.mera_core.model.entities import  Dataset


class FakeFormater(MeraFormaterInterface):
    def format_mera_results(self, list_of_dicts_with_list_of_base_results):
        for a_stuff in list_of_dicts_with_list_of_base_results:
            print a_stuff


executer = QueryExecuter(matcher=get_mera_matcher_with_data(graph_path="../../files/out/usos_graph.ttl",
                                                            ngram_song_path="../../files/out/song_ngrams_usos.json",
                                                            ngram_artist_path="../../files/out/artist_ngrams_usos.json",
                                                            counter_path="../../files/out/counter_usos.json"),
                         formater=FormaterToJson())

# executer = QueryExecuter(matcher=get_empty_mera_matcher(),
#                          formater=FormaterToJson())
res = executer.execute_queries_from_file(
    file_path=rel_path_to_file("../../files/out/cwr-json-to-mera-json/posible_queries.json",
                               __file__))
print res


with open("../../files/in/mera_results_mini_usos.json", "r") as file_io:
    json_matches = file_io.read()
    executer.introduce_json_matches_in_graph(json_matches_str=json_matches,
                                             dataset_obj=Dataset(title="MiDatasetCWR"),
                                             serialization_path="../../files/out/usos_graph_ENRICHED.ttl")


