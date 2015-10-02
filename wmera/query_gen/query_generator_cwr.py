__author__ = 'Dani'
import json
from wmera.utils import decode_dict


_MAIN = 'main_info'
_EXTRA = 'extra_args'
_ISWC = "iswc"

_WRITER = 'writer'
_SONG = 'song'
_ARTIST = 'artist'
_ALT = 'alt'
_ALBUM = 'album'


def process_entry_of_work(data_dict):
    iswc_code = None
    if data_dict[_ISWC] is not None:
        iswc_code = "I-" + str(data_dict[_ISWC]['id_code']) + "-" + str(data_dict[_ISWC]['check_digit'])
    return {_MAIN: data_dict['title'],
            _ISWC: iswc_code}
    # return {_MAIN: data_dict['title']}


def process_entry_of_work_with_author(data_dict):
    name = ""
    if 'writer' in data_dict:
        if 'writer_first_name' in data_dict['writer'] and data_dict['writer']['writer_first_name'] is not None:
            name += data_dict['writer']['writer_first_name']
        if 'writer_last_name' in data_dict['writer'] and data_dict['writer']['writer_last_name'] is not None:
            name += " " + data_dict['writer']['writer_last_name']

    if name != "":
        return {_EXTRA: {_WRITER: [name]}}
    else:
        return {}


def process_entry_of_performer(data_dict):
    name = ""

    if data_dict['performing_artist_first_name'] is not None:
        name += data_dict['performing_artist_first_name']
    if data_dict['performing_artist_last_name'] is not None:
        name += " " + data_dict['performing_artist_last_name']

    if name != "":
        return {_EXTRA: {_ARTIST: [name]}}
    else:
        return {}


def process_entry_of_work_origin(data_dict):
    return {}  # Dunno what to do with this


def process_entry_of_alternate_title(data_dict):
    if data_dict['alternate_title'] not in [None, ""]:
        return {_EXTRA: {_ALT: [data_dict['alternate_title']]}}
    else:
        return None


def process_entry_of_additional_info(data_dict):
    return {}  # Enough


def process_entry_of_compositor(data_dict):
    return {}  # It looks well, but it does not apperar un the CWR, so i don't know the structure TODO


def process_entry_of_title_for_excrepts(data_dict):
    return {}  # Enough


def process_entry_of_interested_party(data_dict):
    return {}  # Enough


def process_entry_of_intrumental_detail(data_dict):
    return {}  # Enough


def process_entry_of_instrumental_summary(data_dict):
    return {}  # Enough


def process_entry_of_message(data_dict):
    return {}  # Enough


def process_entry_of_non_roman_stuff(data_dict):
    return {}  # Enough


def process_entry_of_other_publisher(data_dict):
    return {}  # Enough


def process_entry_of_other_writer(data_dict):
    return process_entry_of_work_with_author(data_dict)


def process_entry_of_publisher_for_writer(data_dict):
    return {}  # Enough


def process_entry_of_recording_detail(data_dict):
    # if data_dict['first_album_title'] not in [None, ""]:
    #     return {_EXTRA: {_ALBUM: [data_dict['first_album_title']]}}
    # else:
    #     return {}
    return {}  # The function works well once we have album processing.


def process_entry_of_publisher_territory_control(data_dict):
    return {}  # Enough


def process_entry_of_publisher_controlled_by_submiter(data_dict):
    return {}  # Enough


def process_entry_of_writer_territory_of_control(data_dict):
    return {}  # Enough


def process_entry_of_terrotory_in_agreement(data_dict):
    return {}  # Enough


def process_entry_of_original_work_title_for_versions(data_dict):
    result = {}
    empty_arr = [None, ""]
    if data_dict['title'] not in empty_arr:
        result = {_EXTRA: {_ALT: [data_dict['title']]}}

    valid_names = []

    name1 = ""
    if data_dict['writer_1_first_name'] is not None:
        name1 += data_dict['writer_1_first_name']
    if data_dict['writer_1_last_name'] is not None:
        name1 += data_dict['writer_1_last_name']
    if name1 != "":
        valid_names.append(name1)

    name2 = ""
    if data_dict['writer_2_first_name'] is not None:
        name2 += data_dict['writer_2_first_name']
    if data_dict['writer_2_last_name'] is not None:
        name2 += data_dict['writer_2_last_name']
    if name2 != "":
        valid_names.append(name2)

    if len(valid_names) == 0:
        return result
    else:
        if _EXTRA not in result:
            result[_EXTRA] = {}
        result[_EXTRA][_WRITER] = []
        for name in valid_names:
            result[_EXTRA][_WRITER].append(name)
        return result


# ###############################################################################


class CWRQueryGenerator(object):
    _func_dict = {'NWR': process_entry_of_work,
                  'SWR': process_entry_of_work_with_author,
                  'PER': process_entry_of_performer,
                  'ORN': process_entry_of_work_origin,
                  'ALT': process_entry_of_alternate_title,
                  'ARI': process_entry_of_additional_info,
                  'COM': process_entry_of_compositor,
                  'EWT': process_entry_of_title_for_excrepts,  # ?
                  'IPA': process_entry_of_interested_party,
                  'IND': process_entry_of_intrumental_detail,
                  'INS': process_entry_of_instrumental_summary,
                  'MSG': process_entry_of_message,
                  'NAT': process_entry_of_non_roman_stuff,
                  'NCT': process_entry_of_non_roman_stuff,
                  'NET': process_entry_of_non_roman_stuff,
                  'NOW': process_entry_of_non_roman_stuff,
                  'NPN': process_entry_of_non_roman_stuff,
                  'NPR': process_entry_of_non_roman_stuff,
                  'NVT': process_entry_of_non_roman_stuff,
                  'NWN': process_entry_of_non_roman_stuff,
                  'OPU': process_entry_of_other_publisher,
                  'OWR': process_entry_of_other_writer,
                  'PWR': process_entry_of_publisher_for_writer,
                  'REC': process_entry_of_recording_detail,
                  'SPT': process_entry_of_publisher_territory_control,
                  'SPU': process_entry_of_publisher_controlled_by_submiter,
                  'SWT': process_entry_of_writer_territory_of_control,
                  'TER': process_entry_of_terrotory_in_agreement,
                  'VER': process_entry_of_original_work_title_for_versions
    }

    def __init__(self, queries_path=None, str_json_content=None, config_path=None):
        if (queries_path is None and str_json_content is None) or (
                        queries_path is not None and str_json_content is not None):
            raise ValueError("One and only one of queries_path or str_json_content should be provided")
        self._str_json_content = str_json_content
        self._queries_path = queries_path
        self._config_path = config_path


    def gen_mera_json(self):
        mera_queries = self.gen_mera_queries()
        mera_config = self.gen_mera_config()
        # return json.dumps({'config': mera_config,
        #                    'queries': mera_queries})
        return {'config': mera_config,
                'queries': mera_queries}

    def gen_mera_config(self):
        return {}  # TODO

    def gen_mera_queries(self):
        original_transactions = self._read_transactions()
        mera_queries = []
        for a_transaction in original_transactions:
            candidate_query = self.gen_query_from_transaction(a_transaction)
            if candidate_query is not None:
                mera_queries.append(candidate_query)
        return mera_queries

    def _read_transactions(self):
        if self._queries_path is not None:
            with open(self._queries_path, "r") as file_queries:  # It is ok
                return json.load(file_queries, object_hook=decode_dict)['transactions']
        else:  # There must be str content
            return json.loads(self._str_json_content, object_hook=decode_dict)['transactions']

    def gen_query_from_transaction(self, transaction):
        result = {'type_of_query': 'find_song'}
        for a_dict in transaction:
            target_function = CWRQueryGenerator._func_dict[a_dict['record_type']]
            self.merge_information_in_query_dict(query_dict=result,
                                                 new_info_dict=target_function(a_dict))
        return result

    def merge_information_in_query_dict(self, query_dict, new_info_dict):
        for key in new_info_dict:
            if key not in query_dict:
                query_dict[key] = new_info_dict[key]
            else:  # We are in a case in which query_dict[key] points to a dict. Otherwise, if it were pointing to a
                # str, it could not be included. There will be information in conflict
                for sub_key in new_info_dict[key]:
                    if not sub_key in query_dict[key]:
                        query_dict[key][sub_key] = new_info_dict[key][sub_key]
                    else:  # query_dict[key][sub_key] must necessarily be a list
                        for new_str_elem in new_info_dict[key][sub_key]:
                            if new_str_elem not in query_dict[key][sub_key]:
                                query_dict[key][sub_key].append(new_str_elem)


    def gen_srialized_mera_json(self, file_path):
        with open(file_path, "w") as result_file:
            json.dump(self.gen_mera_json(), result_file)
            # result_file.write(self.gen_mera_json())






        
        
