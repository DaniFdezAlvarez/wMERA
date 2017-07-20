from apps.discogs_survey_experiment.consts import _CHAR_LOW, _CHAR_MISSED, \
    _POS_FIRST, _POS_MIDDLE_MAX, _CHAR_IGNORE_LINE, _CHAR_SEPARATOR, _CHAR_NA

from apps.discogs_survey_experiment.utils import aceptable_position_chars, is_better_pos


import json

_FIELD_ID = 0
_FIELD_NO_REFS = 1
_FIELD_A_ART = 2
_FIELD_ALL_ART = 3
_FIELD_A_WRI = 4
_FIELD_ALL_WRI = 5
_FIELD_COMBI_SIM = 6
_FIELD_COMBI_ALL = 7
_FIELD_COMMENT = 8

_ARRAY_FIELDS = [_FIELD_NO_REFS, _FIELD_A_ART, _FIELD_ALL_ART, _FIELD_A_WRI,
                 _FIELD_ALL_WRI, _FIELD_COMBI_SIM, _FIELD_COMBI_ALL]

_BEST_AN_ART_OR_WRI = "ART_OR_WRI"
_BEST_WITH_SOME_COMBINATION = "SOME_STORED_COMBINATION"
_TOTALS = -1

_KEY_FIRST_POS = "First"
_KEY_MIDDLE_POS = "Middle"
_KEY_LOW_POS = "Low"
_KEY_MISSED = "missed"
_KEY_NA = "n/a"


class DiscogsSurveyMBExperiment(object):
    def __init__(self, file_path):
        self._file_path = file_path

        self._results = {
            _FIELD_NO_REFS: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _FIELD_A_ART: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _FIELD_ALL_ART: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _FIELD_A_WRI: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            }
            ,
            _FIELD_ALL_WRI: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            }
            ,
            _FIELD_COMBI_SIM: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _FIELD_COMBI_ALL: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _BEST_AN_ART_OR_WRI: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _BEST_WITH_SOME_COMBINATION: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            },
            _TOTALS: {
                _KEY_FIRST_POS: 0,
                _KEY_MIDDLE_POS: 0,
                _KEY_LOW_POS: 0,
                _KEY_MISSED: 0,
                _KEY_NA: 0,
            }
        }
        self._decreasements = 0

    def run(self):
        self._process_source_file()
        return self._generate_report()

    def _generate_report(self):
        return json.dumps(self._results, indent=4) + "\nDecreasements: " + str(self._decreasements)

    def _process_source_file(self):
        with open(self._file_path, "r") as in_stream:
            for line in in_stream:
                self._process_raw_line(line.replace("\n", ""))

    def _process_raw_line(self, line):
        if len(line) == 0 or line.startswith(_CHAR_IGNORE_LINE):
            return
        pieces = line.split(_CHAR_SEPARATOR)
        self._ensure_quality_of_line(pieces, line)
        self._classify_line(pieces)

    def _classify_line(self, splitted_line):
        for a_field in _ARRAY_FIELDS:
            self._process_field_of_a_line(a_field, splitted_line)
        self._process_totals_of_a_line(splitted_line)
        self._process_combination_single_ref(splitted_line)
        self._process_combination_two_or_more_refs(splitted_line)
        self._process_decreasements_of_a_line(splitted_line)

    def _process_any_combination_of_field(self, splitted_line, array_of_fields, dict_key):
        best = _CHAR_NA
        for a_field in array_of_fields:
            if is_better_pos(best, splitted_line[a_field]):
                best = splitted_line[a_field]

        if best == _CHAR_NA:
            self._results[dict_key][_KEY_NA] += 1
        elif best == _CHAR_MISSED:
            self._results[dict_key][_KEY_MISSED] += 1
        elif best == _CHAR_LOW:
            self._results[dict_key][_KEY_LOW_POS] += 1
        else:
            best = int(best)
            if best == _POS_FIRST:
                self._results[dict_key][_KEY_FIRST_POS] += 1
            elif best <= _POS_MIDDLE_MAX:
                self._results[dict_key][_KEY_MIDDLE_POS] += 1
            else:
                self._results[dict_key][_KEY_LOW_POS] += 1

    def _process_totals_of_a_line(self, splitted_line):
        self._process_any_combination_of_field(splitted_line, _ARRAY_FIELDS, _TOTALS)

    def _process_combination_single_ref(self, splitted_line):
        self._process_any_combination_of_field(splitted_line, [_FIELD_A_ART, _FIELD_A_WRI], _BEST_AN_ART_OR_WRI)

    def _process_combination_two_or_more_refs(self, splitted_lines):
        self._process_any_combination_of_field(splitted_lines, [_FIELD_COMBI_ALL, _FIELD_ALL_ART, _FIELD_ALL_WRI],
                                               _BEST_WITH_SOME_COMBINATION)

    def _process_decreasements_of_a_line(self, splitted_line):
        # NO REFS
        if is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_A_ART]) and splitted_line[
            _FIELD_A_ART] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_ALL_ART]) and splitted_line[
            _FIELD_ALL_ART] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_ALL_WRI]) and splitted_line[
            _FIELD_ALL_WRI] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_A_WRI]) and splitted_line[
            _FIELD_A_WRI] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_COMBI_SIM]) and splitted_line[
            _FIELD_COMBI_SIM] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_COMBI_ALL]) and splitted_line[
            _FIELD_COMBI_ALL] != _CHAR_NA:
            self._decreasements += 1

        # AN ART
        elif is_better_pos(splitted_line[_FIELD_A_ART], splitted_line[_FIELD_ALL_ART]) and splitted_line[
            _FIELD_ALL_ART] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_A_ART], splitted_line[_FIELD_COMBI_SIM]) and splitted_line[
            _FIELD_COMBI_SIM] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_A_ART], splitted_line[_FIELD_COMBI_ALL]) and splitted_line[
            _FIELD_COMBI_ALL] != _CHAR_NA:
            self._decreasements += 1

        # A_WRI
        elif is_better_pos(splitted_line[_FIELD_A_WRI], splitted_line[_FIELD_ALL_WRI]) and splitted_line[
            _FIELD_ALL_WRI] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_A_WRI], splitted_line[_FIELD_COMBI_SIM]) and splitted_line[
            _FIELD_COMBI_SIM] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_A_WRI], splitted_line[_FIELD_COMBI_ALL]) and splitted_line[
            _FIELD_COMBI_ALL] != _CHAR_NA:
            self._decreasements += 1

        # ALL_ART
        elif is_better_pos(splitted_line[_FIELD_ALL_ART], splitted_line[_FIELD_COMBI_ALL]) and splitted_line[
            _FIELD_COMBI_ALL] != _CHAR_NA:
            self._decreasements += 1

        # ALL_WRI
        elif is_better_pos(splitted_line[_FIELD_ALL_WRI], splitted_line[_FIELD_COMBI_ALL]) and splitted_line[
            _FIELD_COMBI_ALL] != _CHAR_NA:
            self._decreasements += 1

        # COMBI_SIM
        elif is_better_pos(splitted_line[_FIELD_COMBI_SIM], splitted_line[_FIELD_COMBI_ALL]) and splitted_line[
            _FIELD_COMBI_ALL] != _CHAR_NA:
            self._decreasements += 1

    def _process_field_of_a_line(self, a_field, splitted_line):
        target_data = splitted_line[a_field]
        if target_data == _CHAR_MISSED:
            self._results[a_field][_KEY_MISSED] += 1
        elif target_data == _CHAR_LOW:
            self._results[a_field][_KEY_LOW_POS] += 1
        elif target_data == _CHAR_NA:
            self._results[a_field][_KEY_NA] += 1
        else:
            target_data = int(target_data)
            if target_data == _POS_FIRST:
                self._results[a_field][_KEY_FIRST_POS] += 1
            elif target_data <= _POS_MIDDLE_MAX:
                self._results[a_field][_KEY_MIDDLE_POS] += 1
            else:
                self._results[a_field][_KEY_LOW_POS] += 1

    def _ensure_quality_of_line(self, splitted_line, raw_line):
        if len(splitted_line) < 8:  # Number of fields
            raise BaseException("Not enough fields: " + raw_line)
        try:  # Numeric id
            int(splitted_line[_FIELD_ID].strip())

        except:
            raise BaseException("No numeric id: " + raw_line)

        for a_field in _ARRAY_FIELDS:  # Recognized positions
            if splitted_line[a_field] not in aceptable_position_chars():
                print splitted_line[a_field]
                raise BaseException("Non-acceptable position char: " + raw_line)
