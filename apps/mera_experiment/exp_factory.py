
from apps.mera_experiment.matchers.matcher_ignoring_refinements import MeraMatcherIgnoringRefinements

__author__ = 'Dani'

from rdflib import Graph


def get_mera_matcher_no_refs_with_data(mera_graph, ngram_song_repo, ngram_artist_repo, counter_repo):
    return MeraMatcherIgnoringRefinements(graph=mera_graph,
                                          artist_ngrams_repository=ngram_artist_repo,
                                          song_ngrams_repository=ngram_song_repo,
                                          entity_counter_repository=counter_repo)
