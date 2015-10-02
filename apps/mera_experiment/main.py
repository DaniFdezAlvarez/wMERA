from apps.mera_experiment.mera_experiment import MeraExperiment
from apps.mera_experiment.query_gen.aol_query_gen import AolQueryGen
from apps.mera_experiment.query_gen.musicbrainz_query_gen import MusicbrainzQueryGen


__author__ = 'Dani'

from test.t_utils.t_factory import get_mera_matcher_with_data
from apps.mera_experiment.exp_factory import get_mera_matcher_no_refs_with_data


# ######### COMPLETE WITH REFS
print "---------------- STARTING COMPLETE WITH REFS...."

matcher_complete_with_refs = get_mera_matcher_with_data(graph_path="files/discogs_complete_graph.ttl",
                                                        ngram_song_path="files/song_ngrams_complete.json",
                                                        ngram_artist_path="files/artist_ngrams_complete.json",
                                                        counter_path="files/counter_complete.json")

print "---------------- COMPLETE WITH REFS: Structures loaded"

experiment_aol_complete_refs = MeraExperiment(query_gen=AolQueryGen(matcher=matcher_complete_with_refs,
                                                                    aol_path_file="files/random_aol.txt"),
                                              description="AOL against complete graph with refs")
experiment_mb_complete_refs = MeraExperiment(query_gen=MusicbrainzQueryGen(matcher=matcher_complete_with_refs,
                                                                           musicbrainz_path_file="files/random_musicbrainz.tsv"),
                                             description="MB against a complete graph with refs")



# result = experiment_aol.run()
result_mb_complete_ref = experiment_mb_complete_refs.run()
print result_mb_complete_ref.report
result_aol_complete_refs = experiment_aol_complete_refs.run()
print result_aol_complete_refs.report
result_mb_complete_ref.report_to_file("files/out/res_mb_complete_refs.txt")
result_aol_complete_refs.report_to_file("files/out/res_aol_complete_refs.txt")

print "----------------  COMPLETE WITH REFS ENDED"


# ##############   COMPLETE NO REFS

print "---------------- STARTING COMPLETE NO REFS"

matcher_complete_no_refs = get_mera_matcher_no_refs_with_data(
    mera_graph=matcher_complete_with_refs._graph,
    ngram_artist_repo=matcher_complete_with_refs._repo_artist_ngrams,
    ngram_song_repo=matcher_complete_with_refs._repo_song_ngrams,
    counter_repo=matcher_complete_with_refs._repo_counter)

print "---------------- COMPLETE NO REFS: structures loaded"

experiment_aol_complete_no_refs = MeraExperiment(query_gen=AolQueryGen(matcher=matcher_complete_no_refs,
                                                                       aol_path_file="files/random_aol.txt"),
                                                 description="AOL against a complete graph, no refinements")

experiment_mb_complete_no_refs = MeraExperiment(query_gen=MusicbrainzQueryGen(matcher=matcher_complete_no_refs,
                                                                              musicbrainz_path_file="files/random_musicbrainz.tsv"),
                                                description="MB against a complete graph, no refinements")

result_mb_complete_no_refs = experiment_mb_complete_no_refs.run()
print result_mb_complete_no_refs.report
result_aol_complete_no_refs = experiment_aol_complete_no_refs.run()
print result_aol_complete_no_refs.report

result_mb_complete_no_refs.report_to_file("files/out/res_mb_complete_NO_refs.txt")
result_aol_complete_no_refs.report_to_file("files/out/res_aol_complete_NO_refs.txt")

print "---------------- COMPLETE NO REFS ENDED"

# ######## FREE MEMORY

print "---------------- FREE MEMORY STAGE......"

matcher_complete_with_refs = None
matcher_complete_no_refs = None
experiment_aol_complete_refs = None
experiment_aol_complete_no_refs = None
experiment_mb_complete_no_refs = None
experiment_mb_complete_refs = None



####### ANEMIC WITH REFS

print "---------------- STARTING ANEMIC WITH REFS...."

matcher_anemic_with_refs = get_mera_matcher_with_data(graph_path="files/discogs_anemic_graph.ttl",
                                                      ngram_song_path="files/song_ngrams_anemic.json",
                                                      ngram_artist_path="files/artist_ngrams_anemic.json",
                                                      counter_path="files/counter_anemic.json")

print "---------------- ANEMIC WITH REFS: structures loaded"
experiment_aol_anemic_refs = MeraExperiment(query_gen=AolQueryGen(matcher=matcher_anemic_with_refs,
                                                                  aol_path_file="files/random_aol.txt"),
                                            description="AOL against anemic graph with refs")
experiment_mb_anemic_refs = MeraExperiment(query_gen=MusicbrainzQueryGen(matcher=matcher_anemic_with_refs,
                                                                         musicbrainz_path_file="files/random_musicbrainz.tsv"),
                                           description="MB against a anemic graph with refs")

result_mb_anemic_ref = experiment_mb_anemic_refs.run()
print result_mb_anemic_ref.report
result_aol_anemic_refs = experiment_aol_anemic_refs.run()
print result_aol_anemic_refs.report
result_mb_anemic_ref.report_to_file("files/out/res_mb_anemic_refs.txt")
result_aol_anemic_refs.report_to_file("files/out/res_aol_anemic_refs.txt")

print "---------------- ANEMIC WITH REFS ENDED"



######## ANEMIC NO REFS


print "---------------- STARTING ANEMIC NO REFS...."

matcher_anemic_no_refs = get_mera_matcher_no_refs_with_data(
    mera_graph=matcher_anemic_with_refs._graph,
    ngram_artist_repo=matcher_anemic_with_refs._repo_artist_ngrams,
    ngram_song_repo=matcher_anemic_with_refs._repo_song_ngrams,
    counter_repo=matcher_anemic_with_refs._repo_counter)

print "---------------- ANEMIC NO REFS: Structures loaded"

experiment_aol_anemic_no_refs = MeraExperiment(query_gen=AolQueryGen(matcher=matcher_anemic_no_refs,
                                                                     aol_path_file="files/random_aol.txt"),
                                               description="AOL against anemic graph with NO refs")
experiment_mb_anemic_no_refs = MeraExperiment(query_gen=MusicbrainzQueryGen(matcher=matcher_anemic_no_refs,
                                                                            musicbrainz_path_file="files/random_musicbrainz.tsv"),
                                              description="MB against a anemic graph with NO refs")

result_mb_anemic_no_refs = experiment_mb_anemic_no_refs.run()
print result_mb_anemic_no_refs.report
result_aol_anemic_no_refs = experiment_aol_anemic_no_refs.run()
print result_aol_anemic_no_refs.report
result_mb_anemic_no_refs.report_to_file("files/out/res_mb_anemic_NO_refs.txt")
result_aol_anemic_no_refs.report_to_file("files/out/res_aol_anemic_NO_refs.txt")

print "---------------- ANEMIC NO REFS ENDED"


########### FREE MEMORY

print "---------------- FREE MEMORY SECOND STAGE"

matcher_anemic_no_refs = None
matcher_anemic_with_refs = None
experiment_aol_anemic_no_refs = None
experiment_aol_anemic_refs = None
experiment_mb_anemic_no_refs = None
experiment_mb_anemic_ref = None



###### Trying to persist result objects

print "---------------- TRYING TO SERIALIZE "

result_mb_anemic_ref.serialize_experiment("files/out/srz_mb_anem_refs.smthg")
result_mb_anemic_no_refs.serialize_experiment("files/out/srz_mb_anem_NOrefs.smthg")
result_mb_complete_ref.serialize_experiment("files/out/srz_mb_comp_refs.smthg")
result_mb_complete_no_refs.serialize_experiment("files/out/srz_mb_comp_NOrefs.smthg")

result_aol_anemic_no_refs.serialize_experiment("files/out/srz_aol_anem_NOrefs.smthg")
result_aol_anemic_refs.serialize_experiment("files/out/srz_aol_anem_refs.smthg")
result_aol_complete_refs.serialize_experiment("files/out/srz_aol_comp_refs.smthg")
result_aol_complete_no_refs.serialize_experiment("files/out/srz_aol_comp_NOrefs.smthg")

