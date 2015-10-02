# coding=utf-8
"""
Structure of forms dict and refinements dicts:

FORMS: it contains pairs key value with the form "str_form" : score. The str forms belong
to the entity with uri self._uri. Example:

self._forms = { "Amr de vrano" : 0.9,
                "Amor de verano" : 1.0,
                "Amor de verano MAXIMO" : 0.8
                ...
                }

REFINEMETS: it contains pairs key-value with the form "type_of_refinement" : {dict_of the refinement}.
The dict of the refinements has the next structure:

{
    FORMS_REFINEMENT : { pairs str_form - score
                        }
    RELEVANCE_REFINEMENT : 0.5
    MINIMUM_ACCEPTABLE_SCORE_REFINEMENT : 0.6
    QUERY_REFINEMENT : "A Artist name"
}

a complete example of a random refinement dict would be:

self._refinements = {
                       TYPE_ARTIST_NAME : {
                                            FORMS_REFINEMENT : {
                                                                "Bisbi" : 0.2,
                                                                "David Bisbal" : 1.0,
                                                                "David B." : 0.7,
                                                                },
                                            RELEVANCE_REFINEMENT : 0.8,
                                            MINIMUM_ACCEPTABLE_SCORE_REFINEMENT : 0.6,
                                            QUERY_REFINEMENT : "David Bisbal"
                                           },
                       TYPE_ALBUM_NAME : {
                                            FORMS_REFINEMENT : {
                                                                "Corason latino" : 0.95,
                                                                },
                                            RELEVANCE_REFINEMENT : 0.4,
                                            MINIMUM_ACCEPTABLE_SCORE_REFINEMENT : 0.6,
                                            QUERY_REFINEMENT : "Corazón latino"
                                           },
                        ...
                      }



"""

__author__ = 'Dani'

# from mera.str_ops.str_comp import compare_all_algorithms


FORMS_REFINEMENT = "forms"
RELEVANCE_REFINEMENT = "relevance"
MINIMUM_ACCEPTABLE_SCORE_REFINEMENT = "min_allowed"
QUERIES_REFINEMENT = "query"

TYPE_ARTIST_NAME = "ARTIST"
TYPE_SONG_NAME = "SONG"
TYPE_ALBUM_NAME = "ALBUM"

from wmera.mera_core.str_ops.string_comparator import StringComparator
from wmera.mera_core.str_ops.str_impl.levenshtein import Levenstein
from wmera.mera_core.str_ops.str_impl.weightned_damerau_levenshtein import WeightedDamerauLevenshtein


class MeraBaseResult(object):
    def __init__(self, uri, entity, query):
        """
        Represents the scores obtained after comparing the entity "entity"
        with the URI "uri" in the graph againt the query "query", storing
        all the forms compared and subscores

        :param uri: uri of the entity in the graph
        :param entity: model object used
        :param query: text to compare with the forms of the model object
        :return:
        """
        self._entity = entity
        self._uri = uri
        self._query = query
        self._forms = {}
        self._refinements = {}
        self._comparator = StringComparator([Levenstein, WeightedDamerauLevenshtein])

    @property
    def uri(self):
        return self._uri

    @property
    def entity(self):
        return self._entity

    @property
    def query(self):
        return self._query


    def __cmp__(self, other):
        """
        Criteria:
        It will be considered greater the entity with bigger get_max_score punctuation.

        In case of draw, it will be considered greater the one a higher score in any of
        its primary forms (without refinements).

        In case of draw again, the object with the highest two scores. And so on.

        If we reach the len with a draw in all its elements, it will be considered
        higher the one with the sorter list
        Examples when we obtain the same score in get_max_score(result sorting
        entities with the greater first):

        With this scores: [1,0.43, 0.2]  , [0.99, 0.89, 0.86], we sort like this:

        1. [1,0.43, 0.2]
        2. [0.99, 0.89, 0.86]

        With this scores: [1, 0.90, 0.0]   ,  [1, 0.89, 0.43, 0.42] , we sort like this
         1. [1, 0.90, 0.0]
         2. [1, 0.89, 0.43, 0.42]

        With this scores: [1, 0.89, 0.43]  , [1, 0.89, 0.43, 0.42]
        we sort like this:

        1. [1, 0.89, 0.43]
        2. [1, 0.89, 0.43, 0.42]


        :param other:
        :return:
        """
        if not isinstance(other, MeraBaseResult):
            raise NotImplementedError("Unsupported Comparison")

        self_score = self.get_max_score()
        other_score = other.get_max_score()
        if self_score > other_score:
            return 1
        elif self_score < other_score:
            return -1

        else:
            self_base_scores = self._forms.values()
            self_base_scores.sort(reverse=True)
            other_base_scores = other._forms.values()
            other_base_scores.sort(reverse=True)

            index = 0

            while index < len(self_base_scores) and index < len(other_base_scores):
                if self_base_scores[index] < other_base_scores[index]:
                    return -1
                if self_base_scores[index] < other_base_scores[index]:
                    return 1
                index += 1

            if len(self_base_scores) < len(other_base_scores):
                return 1
            elif len(self_base_scores) > len(other_base_scores):
                return -1

        return 0


    def __str__(self):
        return "{\nCANONICAL: " + self._entity.canonical + "\nFORMS: [" + str(self._forms) + \
               "]\nMAX SCORE WITH REFS: " + str(self.get_max_score()) + "\n"


    def get_refinements(self):
        """

        :return:
        """
        result = []
        for ref_type in self._refinements:
            for a_query in self._refinements[ref_type][QUERIES_REFINEMENT]:
                tmp_dict = {}
                tmp_dict['type'] = ref_type
                tmp_dict['relevance'] = self._refinements[ref_type][RELEVANCE_REFINEMENT]
                tmp_dict['content'] = a_query
                tmp_dict['matched_forms'] = {}
                target_forms = self._refinements[ref_type][QUERIES_REFINEMENT][a_query]
                for a_form in target_forms:
                    tmp_dict['matched_forms'][a_form] = target_forms[a_form]
                result.append(tmp_dict)
        return result

    def add_refinement(self, refinement_type, relevance, minimum_acceptable, query):
        """
        Add a refinement type to the result object. The type provided (through a string) should be included
        in a known range.

        With relevant we are specifying how important is obtaining high coincidences comparing the forms
        (0 the less, 1 the greatest).

        minimum_acceptable specified the minimun score that should be obtained when comparings
        in order to not discard the result (not mattering the relevance factor).

        Query is the string query against we will comparing the forms


        :param refinement_type: string inside a known range of types and used only once with this method
        :param relevance: float between 0 and 1
        :param query: str containing the query against which we are refining
        :param minimum_acceptable: float between 0 and 1
        :return:
        """
        # TODO: revise this doc

        if refinement_type not in self._refinements:
            self._refinements[refinement_type] = {}
            self._refinements[refinement_type][QUERIES_REFINEMENT] = {}
            self._refinements[refinement_type][MINIMUM_ACCEPTABLE_SCORE_REFINEMENT] = minimum_acceptable
            self._refinements[refinement_type][RELEVANCE_REFINEMENT] = relevance

        self._refinements[refinement_type][QUERIES_REFINEMENT][query] = {}

    def add_form_comparison(self, str_form):
        """
        It expects a string to compare it with self._query.
        It compares the query with the received form and stores the result

        :param str_form:
        :return:
        """
        score = self._comparator.compare_str(self._query, str_form)
        self._forms[str_form] = score

    def get_matched_forms(self):
        """
        Return tuples of (form, score)
        :return:
        """
        for a_form in self._forms:
            yield (a_form, self._forms[a_form])


    def add_refinement_form_comparison(self, str_form, refinement_type, query_refinement):
        """
        it compares str_form with self._refinements[refinement_type][QUERY_REFINEMENT],
        and stores the result in self._refinements[refinement_type][FORMS_REFINEMENT]
        if it is >= than self._refinements[refinement_type][MINIMUM_ACCEPTABLE_SCORE_REFINEMENT]
        :param str_form:
        :param refinement_type:
        :return:
        """
        # TODO: revise this doc
        score = self._comparator.compare_str(query_refinement, str_form)
        if score >= self._refinements[refinement_type][MINIMUM_ACCEPTABLE_SCORE_REFINEMENT]:
            self._refinements[refinement_type][QUERIES_REFINEMENT][query_refinement][str_form] = score


    def get_max_score(self):
        """
        It returns a float obtaining form adding the max value in self._forms and all the max
        values of each self_refinements dicts.
        :return:
        """
        max_result = self.get_max_score_without_refinements()
        for a_ref_type_key in self._refinements:
            a_refinement_type = self._refinements[a_ref_type_key]
            for a_ref_query in a_refinement_type[QUERIES_REFINEMENT]:
                if len(a_refinement_type[QUERIES_REFINEMENT][a_ref_query]) > 0:
                    max_result += a_refinement_type[RELEVANCE_REFINEMENT] * max(
                        a_refinement_type[QUERIES_REFINEMENT][a_ref_query].values())
        return max_result


    def get_max_score_without_refinements(self):
        """
         It returns a float with the max value in self._forms
        :return:
        """
        return max(self._forms.values())




