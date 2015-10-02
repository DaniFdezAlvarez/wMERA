__author__ = 'Dani'
import json

from wmera.mera_core.result.formater_interface import MeraFormaterInterface


_TYPE_OF_QUERY = 'type_of_query'
_MAIN = 'main_info'
_EXTRA = 'extra_args'
_ISWC = "iswc"


_WRITER = 'writer'
_SONG = 'song'
_ARTIST = 'artist'
_ALT = 'alt'
_ALBUM = 'album'



class FormaterToJson(MeraFormaterInterface):


    def format_mera_results(self, list_of_dicts_with_list_of_base_results):  # It looks quite simple...
        result = []
        for a_dict in list_of_dicts_with_list_of_base_results:
            a_query_result = {}
            self._complete_with_query(a_query_result, a_dict['query'])
            self._complete_with_results(a_query_result, a_dict['results'])
            result.append(a_query_result)
        return json.dumps(result)


    @staticmethod
    def _complete_with_query(target_dict, info_dict):
        target_dict['query'] = info_dict[_MAIN]
        target_dict['type_of_query'] = info_dict[_TYPE_OF_QUERY]
        target_dict['refinements'] = []
        target_dict['iswc'] = info_dict[_ISWC]
        for an_elem_key in info_dict[_EXTRA]:
            for a_sub_elem in info_dict[_EXTRA][an_elem_key]:
                target_dict['refinements'].append({'type': an_elem_key, 'content': a_sub_elem})


    @staticmethod
    def _complete_with_results(target_dict, info_list):
        target_dict['results'] = []
        for a_result in info_list:
            dict_result = {}
            dict_result['entity'] = a_result.uri
            dict_result['usos_transaction_id'] = a_result.entity.usos_transaction_id
            dict_result['isrc'] = a_result.entity.usos_isrc
            dict_result['raw_score'] = a_result.get_max_score_without_refinements()
            dict_result['refined_score'] = a_result.get_max_score()
            # Matched forms
            tmp_dict_forms = {}
            for a_form in a_result.get_matched_forms():
                tmp_dict_forms[a_form[0]] = a_form[1]
            dict_result['matched_forms'] = tmp_dict_forms
            #Refinement
            dict_result['refinements'] = a_result.get_refinements()
            target_dict['results'].append(dict_result)

