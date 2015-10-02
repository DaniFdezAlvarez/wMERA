__author__ = 'Dani'

from wmera.mera_core.model.entities import Dataset
from wmera.utils import rel_path_to_file
from test.t_utils.t_factory import get_clean_graph_generator_mongo_repos
from wmera.parsers.usos.usos_song_parser import UsosSongParser


parser = UsosSongParser(dataset=Dataset("Uso_bmat2heaven"),
                        source_file=rel_path_to_file(
                            "../../files/mini_usos/mini_bmat2heaven.tsv",
                            __file__))

generator = get_clean_graph_generator_mongo_repos()
generator.generate_turtle_song_graph(file_path=rel_path_to_file("../../files/out/usos_graph.ttl",
                                                                __file__),
                                     song_parser=parser,
                                     isolated=True)
