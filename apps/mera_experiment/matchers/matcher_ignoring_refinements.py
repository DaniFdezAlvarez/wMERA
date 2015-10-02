from wmera.mera_core.str_ops.ngrams import extract_unique_normalized_ngrmas

__author__ = 'Dani'

from wmera.mera_core.mera_matcher.mera_matcher import MeraMatcher


class MeraMatcherIgnoringRefinements(MeraMatcher):
    def __init__(self, graph, artist_ngrams_repository, song_ngrams_repository,
                 entity_counter_repository, match_config=None):
        super(MeraMatcherIgnoringRefinements, self).__init__(graph=graph,
                                                             artist_ngrams_repository=artist_ngrams_repository,
                                                             song_ngrams_repository=song_ngrams_repository,
                                                             entity_counter_repository=entity_counter_repository,
                                                             match_config=match_config)

    def find_song(self, name, alt_titles=None, artists=None, collaborators=None, album=None, genres=None):
        ngrmas = extract_unique_normalized_ngrmas(name)
        candidate_songs = self._get_songs_with_best_idf(ngrmas, self._match_config.top_k_blocking_function())
        candidate_songs = self._get_most_similar_songs(original_str=name,
                                                       candidate_songs=candidate_songs,
                                                       top_k_results=self._match_config.top_k_results())

        return candidate_songs

