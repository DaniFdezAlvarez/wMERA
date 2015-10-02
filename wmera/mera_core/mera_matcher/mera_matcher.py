__author__ = 'Dani'

import math
import logging

from wmera.mera_core.str_ops.ngrams import extract_unique_normalized_ngrmas
from wmera.mera_core.result.base_result import MeraBaseResult, TYPE_ARTIST_NAME
from wmera.infrastrusture.mongo.ngrams.mongo_entity_ngrams import NUM_APPARITIONS, ENTITIES
from wmera.mera_core.mera_matcher.match_config import MeraMatchConfig
from wmera.mera_core.mera_matcher.json_to_match_config import ORDER_FIND_SONG, TYPE_ARTIST, TYPE_SONG


class MeraMatcher(object):
    def __init__(self, graph, artist_ngrams_repository, song_ngrams_repository,
                 entity_counter_repository, match_config=None):
        """

        :param graph: it should be an object implementing the interface MeraGraph
                and it should be provided
        """
        self._graph = graph
        self._repo_artist_ngrams = artist_ngrams_repository
        self._repo_song_ngrams = song_ngrams_repository
        self._repo_counter = entity_counter_repository

        self._match_config = match_config
        if match_config is None:
            self._match_config = MeraMatchConfig()
        self._log = logging.getLogger(__name__)


    def find_artist(self, name, country=None, songs=None, albums=None, namevars=None, genres=None):
        """
        Name should be provided and should be an string.
        Country is optional and is expected to be a string.
        The rest of the params could be an string or a list of strings,
        and they are optional.

        The method returns...
        :param name:
        :param songs:
        :param albums:
        :param namevars:
        :param genres:
        :return:
        """
        # TODO: right now, just working with name
        ngrmas = extract_unique_normalized_ngrmas(name)  # Done
        candidate_artists = self._get_artist_with_best_idf(ngrmas, self._match_config.top_k_blocking_function())  # Done
        candidate_artists = self._get_most_similar_artist(original_str=name,
                                                          candidate_artist=candidate_artists,
                                                          top_k_results=self._match_config.top_k_results())  # Done
        return candidate_artists  # TODO : just adapt to other possible and probable formats.
        # TODO but the main work (for name) is done


    def find_artist_group(self, name, country=None, members=None, songs=None, albums=None, namevars=None, genres=None):
        """
        Name should be provided and should be an string.
        Country is optional and is expected to be a string.
        The rest of the params could be an string or a list of strings,
        and they are optional.

        The method returns...

        :param name:
        :param members:
        :param songs:
        :param albums:
        :param namevars:
        :param genres:
        :return:
        """
        pass


    def find_artist_person(self, name, country=None, civil=None, songs=None, albums=None, namevars=None, genres=None):
        """
        Name should be provided and should be an string.
        Civil and country are optional and they are expected to be a string.
        The rest of the params could be an string or a list of strings,
        and they are optional.

        The method returns...
        :param name:
        :param civil:
        :param songs:
        :param albums:
        :param namevars:
        :param genres:
        :return:
        """
        pass

    def find_song(self, name, alt_titles=None, artists=None, collaborators=None, album=None, genres=None):
        ngrmas = extract_unique_normalized_ngrmas(name)
        candidate_songs = self._get_songs_with_best_idf(ngrmas, self._match_config.top_k_blocking_function())
        candidate_songs = self._get_most_similar_songs(original_str=name,
                                                       candidate_songs=candidate_songs,
                                                       top_k_results=self._match_config.top_k_results())
        if artists is not None:
            for an_artist in artists:
                candidate_songs = self._refine_songs_by_artist_name(candidate_songs, an_artist)
        candidate_songs = self._discard_results_with_low_total_score(candidate_songs, ORDER_FIND_SONG)
        candidate_songs.sort(reverse=True)

        return candidate_songs[:self._match_config.top_k_results()]




    def _refine_songs_by_artist_name(self, str_cmp_ordered_candidates, artist_name):
        for a_mera_base_result in str_cmp_ordered_candidates:
            song_uri = a_mera_base_result.uri
            a_mera_base_result.add_refinement(refinement_type=TYPE_ARTIST_NAME,
                                              relevance=self._match_config.get_command_relevance_of_a_type(
                                                  command_name=ORDER_FIND_SONG,
                                                  target_type=TYPE_ARTIST),
                                              minimum_acceptable=self._match_config.get_minimum_of_type(TYPE_ARTIST),
                                              query=artist_name)
            for an_artist in self._graph.get_artists_and_collaborators_of_song_by_uri(song_uri):
                if an_artist.canonical not in ["", None]:
                    for a_form in an_artist.identifying_form_tuples:
                        a_mera_base_result.add_refinement_form_comparison(refinement_type=TYPE_ARTIST_NAME,
                                                                          str_form=a_form[0],
                                                                          query_refinement=artist_name)
        str_cmp_ordered_candidates.sort(reverse=True)
        return str_cmp_ordered_candidates


    def _get_artist_with_best_idf(self, ngrams, top_k=10):
        return self._get_entities_with_best_idf(ngrams=ngrams,
                                                repo=self._repo_artist_ngrams,
                                                num_entities=self._repo_counter.number_of_artists(),
                                                top_k=top_k)

    def _get_songs_with_best_idf(self, ngrams, top_k=10):
        return self._get_entities_with_best_idf(ngrams=ngrams,
                                                repo=self._repo_song_ngrams,
                                                num_entities=self._repo_counter.number_of_songs(),
                                                top_k=top_k)

    def _get_entities_with_best_idf(self, ngrams, repo, num_entities, top_k):
        entities_idf_dict = {}
        entities_ngrams = {}

        for ngram in ngrams:
            ngram_info = repo.get_ngram_info(ngram)
            if ngram_info is not None:
                ngram_apparitions = ngram_info[NUM_APPARITIONS]
                ngram_idf = MeraMatcher._calculate_ngram_idf(num_apparitions=ngram_apparitions,
                                                             max_apparitions=num_entities)
                for entity_with_idf in ngram_info[ENTITIES]:
                    # Looking for artist with max_ngram num
                    if entity_with_idf not in entities_ngrams:
                        entities_ngrams[entity_with_idf] = 1
                    else:
                        entities_ngrams[entity_with_idf] += 1

                    # Normally calculating idfs and so on
                    idf_to_add = ngram_idf * ngram_info[ENTITIES][entity_with_idf]
                    if entity_with_idf not in entities_idf_dict:
                        entities_idf_dict[entity_with_idf] = idf_to_add
                    else:
                        entities_idf_dict[entity_with_idf] += idf_to_add
        resulting_uris = []
        num_ngrams = len(ngrams)
        for entity_with_idf in entities_ngrams:
            if entities_ngrams[entity_with_idf] == num_ngrams:
                resulting_uris.append(entity_with_idf)
                del entities_idf_dict[entity_with_idf]
        for entity_with_idf in self._filter_entities_with_best_idf(entities_idf_dict, top_k):
            resulting_uris.append(entity_with_idf[0])

        return resulting_uris


    @staticmethod
    def _filter_entities_with_best_idf(entities_dict, top_k):
        """
        It returns a generator yielding tuples with:
        first pos: UIR
        second pos: idf socre

        The returned tuples won't be more than top_k and they will
        be yielded in decreasing order

        :param entities_dict:
        :param top_k:
        :return:
        """
        if len(entities_dict) < top_k:
            top_k = len(entities_dict)
        items = entities_dict.items()
        items.sort(key=lambda x: x[1], reverse=True)
        yielded = 0
        for entity_with_idf in items:
            yield entity_with_idf
            yielded += 1
            if yielded >= top_k:
                break


    @staticmethod
    def _calculate_ngram_idf(num_apparitions, max_apparitions):
        return math.log(max_apparitions / num_apparitions)


    def _get_most_similar_artist(self, original_str, candidate_artist, top_k_results):
        """

        :param original_str:
        :param candidate_artist:
        :param top_k_results:
        :return:
        """
        return self._get_most_similar_entities(original_str=original_str,
                                               candidate_entities=candidate_artist,
                                               function_to_find_entity=self._graph.get_artist_by_uri,
                                               top_k_results=top_k_results,
                                               main_type=TYPE_ARTIST)

    def _get_most_similar_songs(self, original_str, candidate_songs, top_k_results):
        """

        :param original_str:
        :param candidate_songs:
        :param top_k_results:
        :return:
        """
        return self._get_most_similar_entities(original_str=original_str,
                                               candidate_entities=candidate_songs,
                                               function_to_find_entity=self._graph.get_song_by_uri,
                                               top_k_results=top_k_results,
                                               main_type=TYPE_SONG)


    def _get_most_similar_entities(self, original_str, candidate_entities, function_to_find_entity, top_k_results, main_type):
        """
        1 We take every identifying form of each entity
        2 We built a MeraBaseResult for each entity
        3 We return a list sorted with the results (just the top_k elements)

        :param original_str:
        :param candidate_entities:
        :param function_to_find_entity: function to track an appropriated object using an URI of candidate_artist
        :param top_k_results:
        :return:
        """
        results = []
        for entity_uri in candidate_entities:
            entity = function_to_find_entity(entity_uri)
            if entity is not None:
                entity_result = MeraBaseResult(entity=entity,
                                               query=original_str,
                                               uri=entity_uri)
                for form_tuple in entity.identifying_form_tuples:  # Receives tuples (str, [list of sources])
                    entity_result.add_form_comparison(form_tuple[0])
                results.append(entity_result)
            else:
                self._log.warning("Corrupted entity in graph (no canonical name): " + entity_uri)

        results = self._discard_results_with_low_main_type(results, main_type)
        return results


    def _discard_results_with_low_total_score(self, results, target_order):
        index_to_discard = []
        for i in range(0, len(results)):
            if results[i].get_max_score() < self._match_config.get_command_threshold(target_order):
                index_to_discard.append(i)
        while len(index_to_discard) != 0:
            index = index_to_discard.pop()
            del results[index]
        return results

    def _discard_results_with_low_main_type(self, results, target_type):
        index_to_discard = []
        for i in range(0, len(results)):
            if results[i].get_max_score_without_refinements() < self._match_config.get_minimum_of_type(target_type):
                index_to_discard.append(i)
        while len(index_to_discard) != 0:
            index = index_to_discard.pop()
            del results[index]
        return results