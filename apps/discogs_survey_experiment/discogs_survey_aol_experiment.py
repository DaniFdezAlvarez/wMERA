
from apps.discogs_survey_experiment.consts import _CHAR_LOW, _CHAR_MISSED, \
    _POS_FIRST, _POS_MIDDLE_MAX, _CHAR_IGNORE_LINE, _CHAR_SEPARATOR, _CHAR_NA

from apps.discogs_survey_experiment.utils import array_str_ints, \
    aceptable_position_chars, is_better_pos

import json


_FIELD_ID = 0
_FIELD_NO_REFS = 1
_FIELD_A_REF = 2
_FIELD_ALL_REFS = 3
_FIELD_COMMENT = 4


_TOTALS = -1

_KEY_FIRST_POS = "First"
_KEY_MIDDLE_POS = "Middle"
_KEY_LOW_POS = "Low"
_KEY_MISSED = "missed"
_KEY_NA = "n/a"

class DiscogsSurveyAOLExperiment(object):

    def __init__(self, file_path):
        self._file_path = file_path

        self._results = {
            _FIELD_NO_REFS : {
                _KEY_FIRST_POS : 0,
                _KEY_MIDDLE_POS : 0,
                _KEY_LOW_POS : 0,
                _KEY_MISSED : 0,
                _KEY_NA : 0,
            },
            _FIELD_A_REF : {
                _KEY_FIRST_POS : 0,
                _KEY_MIDDLE_POS : 0,
                _KEY_LOW_POS : 0,
                _KEY_MISSED : 0,
                _KEY_NA : 0,
            },
            _FIELD_ALL_REFS : {
                _KEY_FIRST_POS : 0,
                _KEY_MIDDLE_POS : 0,
                _KEY_LOW_POS : 0,
                _KEY_MISSED : 0,
                _KEY_NA : 0,
            },
            _TOTALS : {
                _KEY_FIRST_POS : 0,
                _KEY_MIDDLE_POS : 0,
                _KEY_LOW_POS : 0,
                _KEY_MISSED : 0,
                _KEY_NA : 0,
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
        for a_field in [_FIELD_NO_REFS, _FIELD_A_REF, _FIELD_ALL_REFS]:
            self._process_field_of_a_line(a_field, splitted_line)
        self._process_totals_of_a_line(splitted_line)
        self._process_decreasements_of_a_line(splitted_line)


    def _process_totals_of_a_line(self, splitted_line):
        best = _CHAR_NA
        for a_field in [_FIELD_NO_REFS, _FIELD_A_REF, _FIELD_ALL_REFS]:
            if is_better_pos(best, splitted_line[a_field]):
                best = splitted_line[a_field]


        if best == _CHAR_NA:
            self._results[_TOTALS][_KEY_NA] += 1
        elif best == _CHAR_MISSED:
            self._results[_TOTALS][_KEY_MISSED] += 1
        elif best == _CHAR_LOW:
            self._results[_TOTALS][_KEY_LOW_POS] += 1
        else:
            best = int(best)
            if best == _POS_FIRST:
                self._results[_TOTALS][_KEY_FIRST_POS] += 1
            elif best <= _POS_MIDDLE_MAX:
                self._results[_TOTALS][_KEY_MIDDLE_POS] += 1
            else:
                self._results[_TOTALS][_KEY_LOW_POS] += 1

    def _process_decreasements_of_a_line(self, splitted_line):
        if is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_A_REF]) and splitted_line[_FIELD_A_REF] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_NO_REFS], splitted_line[_FIELD_ALL_REFS]) and splitted_line[_FIELD_ALL_REFS] != _CHAR_NA:
            self._decreasements += 1
        elif is_better_pos(splitted_line[_FIELD_A_REF], splitted_line[_FIELD_ALL_REFS]) and splitted_line[_FIELD_ALL_REFS] != _CHAR_NA:
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
        if len(splitted_line) < 4:  # Number of fields
            raise BaseException("Not enough fields: " + raw_line)
        try:  # Numeric id
            int(splitted_line[_FIELD_ID].strip())

        except:
            raise BaseException("No numeric id: " + raw_line)

        for a_field in [_FIELD_NO_REFS, _FIELD_A_REF, _FIELD_ALL_REFS]:  # Recognized positions
            if splitted_line[a_field] not in aceptable_position_chars():
                # print splitted_line[a_field]
                raise BaseException("Non-acceptable position char: " + raw_line)



