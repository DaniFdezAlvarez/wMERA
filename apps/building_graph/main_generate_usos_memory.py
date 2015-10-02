__author__ = 'Dani'

from wmera.mera_core.model.entities import Dataset
from wmera.utils import rel_path_to_file
from test.t_utils.t_factory import get_clean_graph_generator_memory_repos
from wmera.parsers.usos.usos_song_parser import UsosSongParser


parser = UsosSongParser(dataset=Dataset("Uso_bmat2heaven"),
                        source_file=rel_path_to_file(
                            "../../files/mini_usos/mini_bmat2heaven.tsv",
                            __file__))

generator = get_clean_graph_generator_memory_repos()
generator.generate_turtle_song_graph(file_path=rel_path_to_file("../../files/out/usos_graph.ttl",
                                                                __file__),
                                     song_parser=parser,
                                     isolated=True)

generator._repo_artists.save_content(rel_path_to_file("../../files/out/artist_ngrams_usos.json",
                                                      __file__))
generator._repo_songs.save_content(rel_path_to_file("../../files/out/song_ngrams_usos.json",
                                                      __file__))
generator._repo_counter.save_content(rel_path_to_file("../../files/out/counter_usos.json",
                                                      __file__))



