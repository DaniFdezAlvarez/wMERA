__author__ = 'Dani'

import re

from wmera.utils import rel_path_to_file


_WHITE_SPACES = re.compile("  +")
_COMPLEX_STRUCTURE_PATTERN = re.compile(" \- |\- | \-")
_CONTAINS_INFO_PATTERN = re.compile(".*[a-zA-z]+.*")
_COMPLEX_STRUCTURE_TOKENS = [" - ", " -", "- "]

_FEAT_CHARS_OPEN = ["(", " ", "_", "-", ","]
_FEAT_CHARS_CLOSE = [")", " ", "_", "-"]

_NOISY_CHARS_CLOSE_BEG = [".", ",", " ", "(", "-", ":"]

_NOISY_CHARS_OPEN_MID = ["(", " ", "_", ",", ".", "-"]
_NOISY_CHARS_CLOSE_MID = [")", " ", "_", ",", ".", "-"]

_NOISY_CHARS_OPEN_END = [".", ",", " ", ")", "-", ":"]


def serialize_simple_dict(a_dict, file_path):
    with open(file_path, "w") as file_target:
        for a_key in a_dict:
            file_target.write(a_key + "\t" + str(a_dict[a_key]) + "\n")


def serialize_list(a_list,file_path):
    with open(file_path, "w") as file_target:
        for an_elem in a_list:
            file_target.write(an_elem+"\n")


class AolNoisyQueryExtractor(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._feat_vars = self._generate_feat_vars()
        self._noisy_words_beg, self._noisy_words_middle, self._noisy_words_end = self._generate_noisy_words()


    def _generate_noisy_words(self):
        result_middle = []
        result_beg = []
        result_end = []
        with open("../files/consultas_aol/noisy_words.txt") as file_noisy_words:
            for line in file_noisy_words:
                if line.strip() not in ["", "\n", "\r"]:
                    base = line.strip()
                    for a_op in _NOISY_CHARS_OPEN_MID:
                        for a_clo in _NOISY_CHARS_CLOSE_MID:
                            result_middle.append(a_op + base + a_clo)
                    for a_clo in _NOISY_CHARS_CLOSE_BEG:
                        result_beg.append(base + a_clo)
                    for a_op in _NOISY_CHARS_OPEN_END:
                        result_end.append(a_op + base)
        return result_beg, result_middle, result_end


    def _generate_feat_vars(self):
        result = []
        with open("../../files/consultas_aol/feat_vars.txt") as file_feat_vars:
            for line in file_feat_vars:
                if line.strip() not in ["", "\n", "\r"]:
                    base = line.strip()
                    for a_opener in _FEAT_CHARS_OPEN:
                        for a_closer in _FEAT_CHARS_CLOSE:
                            result.append(a_opener + base + a_closer)
        return result

    def run(self):
        queries_with_feat = self._find_queries_with_feat()
        serialize_simple_dict(queries_with_feat, "queries_with_feat.txt")
        # queries_with_feat = self._read_queries_with_feat()  # Short path when already parsed
        candidate_artist, candidate_songs = self._look_for_candidate_artists_and_songs(queries_with_feat)
        candidate_artist = self.clean_noisy_candidates(candidate_artist)  # Returns a list
        candidate_songs = self.clean_noisy_candidates(candidate_songs)  # Returns a list
        serialize_list(candidate_artist, "extracted_artist.txt")
        serialize_list(candidate_songs, "extracted_songs.txt")
        # definitive_queries = self._build_queries_from_candidates(candidate_songs, candidate_artist)
        # with open("result_file.txt", "w") as result_file:
        #     for query in definitive_queries:
        #         result_file.write(query + "\n")


    def clean_noisy_candidates(self, dict_of_candidates):
        result = []
        for a_candidate in dict_of_candidates:
            if len(a_candidate) >= 3:
                if re.match(_CONTAINS_INFO_PATTERN, a_candidate):
                    result.append(a_candidate.strip())
        return result


    def _build_queries_from_candidates(self, candidate_songs, candidate_artist):
        result = []
        failed_lines = []
        with open("../files/consultas_aol/consultas-AOL.txt") as in_file:
            tmp_line = ""
            counter = 0
            for line in in_file:
                try:
                    counter += 1
                    if counter % 50000 == 0:
                        print counter
                        # break
                    tmp_line = line.split("\t")
                    if len(tmp_line) == 2:
                        # print "1-----", tmp_line
                        tmp_line = self._erase_noisy_words(tmp_line[1].strip().lower())
                        # print "2-----", tmp_line
                        detected_as_complex = None
                        for a_song in candidate_songs:
                            if a_song in tmp_line:
                                # if self.line_contains_song_or_artist(tmp_line, a_song):
                                if detected_as_complex is None:
                                    if self._is_complex_structure(tmp_line):
                                        detected_as_complex = True
                                        break
                                    else:
                                        detected_as_complex = False
                                else:
                                    self.append_not_none(result,
                                                         self._build_query_from_candidate_song_and_line(tmp_line,
                                                                                                        a_song))
                        if detected_as_complex is True:
                            self.append_not_none(result, self._build_query_from_complex_structure(tmp_line))
                        else:
                            for an_artist in candidate_artist:
                                if an_artist in tmp_line:
                                    # if self.line_contains_song_or_artist(tmp_line, an_artist):
                                    if detected_as_complex is None:
                                        if self._is_complex_structure(tmp_line):
                                            detected_as_complex = True
                                            break
                                    self.append_not_none(result,
                                                         self._build_query_from_candidate_artist_and_line(tmp_line,
                                                                                                          an_artist))
                            if detected_as_complex is True:
                                self.append_not_none(result, self._build_query_from_complex_structure(tmp_line))
                except:
                    failed_lines.append(line)  # A line failed
        print "-----"
        print len(failed_lines), "lines failed:"
        for line in failed_lines:
            print line
        print "-----"

        return result

    def append_not_none(self, a_list, an_elem):
        if an_elem is not None:
            a_list.append(an_elem)


    def _build_query_from_candidate_song_and_line(self, line, candidate_song):
        for a_feat_var in self._feat_vars:
            if a_feat_var in line:
                tmp_line = line.replace(candidate_song, " ")
                tmp_line = tmp_line.split(a_feat_var)
                return self._build_query_from_all_parsed_fields(main_artist=tmp_line[0],
                                                                feat_artist=tmp_line[1],
                                                                song=candidate_song)

        return self._build_query_from_all_parsed_fields(song=candidate_song,
                                                        main_artist=line.replace(candidate_song, " "),
                                                        feat_artist="")

    def _build_query_from_candidate_artist_and_line(self, line, candidate_artist):
        for a_feat_var in self._feat_vars:
            if a_feat_var in line:
                tmp_line = line.replace(candidate_artist, " ")
                tmp_line = tmp_line.split(a_feat_var)
                return self._build_query_from_all_parsed_fields(main_artist=candidate_artist,
                                                                feat_artist=tmp_line[1],
                                                                song=tmp_line[0])

        return self._build_query_from_all_parsed_fields(main_artist=candidate_artist,
                                                        song=line.replace(candidate_artist, " "),
                                                        feat_artist="")

    def _is_complex_structure(self, norm_query):
        for a_complex_var in _COMPLEX_STRUCTURE_TOKENS:
            if a_complex_var in norm_query:
                for a_feat_var in self._feat_vars:
                    if a_feat_var in norm_query:
                        if self._overlaped_tokens(index1=norm_query.find(a_complex_var),
                                                  tok1=a_complex_var,
                                                  index2=norm_query.find(a_feat_var),
                                                  tok2=a_feat_var):
                            return False
                        else:
                            return True
                return False  # We have checked that there is a complex_var but not a feat_var

    def _build_query_from_complex_structure(self, norm_query):
        song = ""
        main_artist = ""
        feat_artist = ""
        for feat_var in self._feat_vars:
            if feat_var in norm_query:
                index_feat = norm_query.find(feat_var)
                for complex_var in _COMPLEX_STRUCTURE_TOKENS:
                    if complex_var in norm_query:
                        index_complex = norm_query.find(complex_var)
                        if index_complex < index_feat:  # Case song - artist feat artist
                            tmp_pieces = norm_query.split(feat_var)
                            feat_artist = tmp_pieces[1].strip()
                            tmp_pieces = tmp_pieces[0].split(complex_var)
                            main_artist = tmp_pieces[1].strip()
                            song = tmp_pieces[0].strip()
                        else:  # Case artist feat artist - song
                            tmp_pieces = norm_query.split(feat_var)
                            main_artist = tmp_pieces[0].strip()
                            tmp_pieces = tmp_pieces[1].split(complex_var)
                            feat_artist = tmp_pieces[0].strip()
                            song = tmp_pieces[1].strip()
                        break

                break
        return self._build_query_from_all_parsed_fields(main_artist=main_artist,
                                                        feat_artist=feat_artist,
                                                        song=song)


    def _build_query_from_all_parsed_fields(self, main_artist, feat_artist, song):
        song = song.strip()
        feat_artist = feat_artist.strip()
        main_artist = main_artist.strip()
        if len(song) >= 3 and re.match(_CONTAINS_INFO_PATTERN, song) and \
                (re.match(_CONTAINS_INFO_PATTERN, main_artist) or re.match(_CONTAINS_INFO_PATTERN, feat_artist)):
            return song + "\t" + main_artist + "\t" + feat_artist
        else:
            return None


    def _read_queries_with_feat(self):
        result = []
        with open("queries_with_feat.txt", "r") as in_file:
            for line in in_file:
                if "\t" in line:
                    result.append(line.split("\t")[0])
        return result


    def _look_for_candidate_artists_and_songs(self, queries_with_feat):
        dict_songs = {}
        dict_artist = {}
        for a_query in queries_with_feat:
            norm_query = self._erase_noisy_words(a_query)
            if re.search(_COMPLEX_STRUCTURE_PATTERN, norm_query):
                tmp_artist, tmp_songs = self._find_artists_and_songs_in_complex_structure(norm_query)
            else:
                tmp_artist, tmp_songs = self._find_artists_and_songs_in_simple_structure(norm_query)

            for an_artist in tmp_artist:
                if an_artist in dict_artist:
                    dict_artist[an_artist] += 1
                else:
                    dict_artist[an_artist] = 1

            for a_song in tmp_songs:
                if a_song in dict_songs:
                    dict_songs[a_song] += 1
                else:
                    dict_songs[a_song] = 1

        return dict_artist, dict_songs


    def _find_artists_and_songs_in_simple_structure(self, norm_query):
        list_artist = []
        list_songs = []
        for feat_var in self._feat_vars:
            if feat_var in norm_query:
                tmp_pieces = norm_query.split(feat_var)
                list_artist.append(tmp_pieces[1].strip())
                list_songs.append(tmp_pieces[0].strip())
                break
        return list_artist, list_songs

    def _find_artists_and_songs_in_complex_structure(self, norm_query):
        """
        Different ways to proceed if we find the "-" before of after the "feat".
        If it is before, the structure could be like:
        SONG_TITLE  - MAIN_ARTIST FEAT FEAT_ARTIST

        If it is after, the structure could be like:
        MAIN_ARTIST feat FEAT_ARTIST - SONG_TITLE

        :param norm_query:
        :return:
        """
        list_artist = []
        list_songs = []
        for feat_var in self._feat_vars:
            if feat_var in norm_query:
                index_feat = norm_query.find(feat_var)
                for complex_var in _COMPLEX_STRUCTURE_TOKENS:
                    if complex_var in norm_query:
                        index_complex = norm_query.find(complex_var)
                        if self._overlaped_tokens(index_feat, feat_var, index_complex, complex_var):
                            return self._find_artists_and_songs_in_simple_structure(norm_query)
                        if index_complex < index_feat:  # Case song - artist feat artist
                            tmp_pieces = norm_query.split(feat_var)
                            list_artist.append(tmp_pieces[1].strip())
                            tmp_pieces = tmp_pieces[0].split(complex_var)
                            list_artist.append(tmp_pieces[1].strip())
                            list_songs.append(tmp_pieces[0].strip())
                        else:  # Case artist feat artist - song
                            tmp_pieces = norm_query.split(feat_var)
                            list_artist.append(tmp_pieces[0].strip())
                            tmp_pieces = tmp_pieces[1].split(complex_var)
                            list_artist.append(tmp_pieces[0].strip())
                            list_songs.append(tmp_pieces[1].strip())
                        break

                break
        return list_artist, list_songs


    def _overlaped_tokens(self, index1, tok1, index2, tok2):
        if index1 == index2:
            return True
        elif index1 < index2:
            if len(tok1) + index1 >= index2:
                return True
            else:
                return False
        else:
            if len(tok2) + index2 >= index1:
                return True
            else:
                return False

    def _get_complex_candidates(self):
        # If we are parsing a piece of an artist, if a char "-" appear it usually mean that
        # the first part is a featuring artist and the second one
        pass


    def _erase_noisy_words(self, query):
        result = query
        for a_mid in self._noisy_words_middle:
            if a_mid in result:
                result = result.replace(a_mid, " ")
        for a_beg in self._noisy_words_beg:
            if result.startswith(a_beg):
                result = result[len(a_beg):]
        for an_end in self._noisy_words_end:
            if result.endswith(an_end):
                result = result[:len(result) - len(an_end)]
        result = " " + result + " "
        result = re.sub(_WHITE_SPACES, " ", result)
        return result


    def _find_queries_with_feat(self):
        result = {}
        with open("../files/consultas_aol/consultas-AOL.txt") as in_file:
            tmp_line = ""
            counter = 0
            for line in in_file:
                counter += 1
                if counter % 100000 == 0:
                    print counter
                tmp_line = line.split("\t")
                if len(tmp_line) == 2:
                    tmp_line = tmp_line[1].strip().lower()
                    for a_feat_var in self._feat_vars:
                        if a_feat_var in tmp_line:
                            # print tmp_line
                            if tmp_line in result:
                                result[tmp_line] += 1
                            else:
                                result[tmp_line] = 1
                            break
        return result






##############

extractor = AolNoisyQueryExtractor(rel_path_to_file("../files/consultas_aol/", __file__))
extractor.run()
