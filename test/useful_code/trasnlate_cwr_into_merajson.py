__author__ = 'Dani'

from wmera.query_gen.query_generator_cwr import CWRQueryGenerator
from wmera.utils import rel_path_to_file

query_gen = CWRQueryGenerator(
    queries_path=rel_path_to_file("../../files/in/cwr-json-to-mera-json/works_group_full.json",
                                  __file__),
    config_path="Doesntmatteryet")
query_gen.gen_srialized_mera_json(file_path="../../files/out/cwr-json-to-mera-json/posible_queries.json")


