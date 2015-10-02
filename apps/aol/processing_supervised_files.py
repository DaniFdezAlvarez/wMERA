__author__ = 'Dani'

_FIELD_SEPARATOR = "####"
_ENTITY_SEPARATOR = '\t'
_RESULT_SEPARATOR = '\t'

_QUERY_INDEX = 0
_FLAGS_INDEX = 1
_COMMENT_INDEX = 2

_MODIFIED_CONTENT_INDEX = 2
_MODIFIED_COMMENT_INDEX = 3


class LineProcessor(object):
    def __init__(self, path_source, path_clean, path_noisy, path_discarded,
                 path_mixed, path_error, localizator_mark, artist_processor=None):
        self._path_source = path_source
        self._path_clean = path_clean
        self._path_noisy = path_noisy
        self._path_discarded = path_discarded
        self._path_mixed = path_mixed
        self._path_error = path_error

        self._localizator_mark = localizator_mark

        self._clean_set = set()
        self._noisy_set = set()
        self._mixed_set = set()

        self._clean_lines = []
        self._noisy_lines = []
        self._mixed_lines = []
        self._discarded_lines = []
        self._errors = []

        self._artist_processor = artist_processor


    def run(self):
        with open(self._path_source, "r") as source_file:
            counter = 1
            for a_line in source_file:
                self.process_line(a_line.replace("\n", ""), counter)
                counter += 1

    def save_content(self):
        print "Saving content..."
        self.save_set_plus_list_content(a_set=self._clean_set,
                                        a_list=self._clean_lines,
                                        a_path=self._path_clean)
        self.save_set_plus_list_content(a_set=self._noisy_set,
                                        a_list=self._noisy_lines,
                                        a_path=self._path_noisy)
        self.save_set_plus_list_content(a_set=self._mixed_set,
                                        a_list=self._mixed_lines,
                                        a_path=self._path_mixed)
        self.save_list_content(a_list=self._discarded_lines,
                               a_path=self._path_discarded)
        if len(self._errors) == 0:
            print "There were no errors"
        else:
            print "There were", len(self._errors), "errors"
            self.save_list_content(a_list=self._errors,
                                   a_path=self._path_error)
        print "Content saved"
        

    def save_list_content(self, a_list, a_path):
        text_list = ""
        for a_elem in a_list:
            text_list += a_elem + "\n"
        text_list = text_list[:-1]
        with open(a_path, "w") as target_file:
            target_file.write(text_list)

    def save_set_plus_list_content(self, a_set, a_list, a_path):
        line_set = ""
        for a_elem in a_set:
            line_set += "||" + a_elem
        line_set = line_set[2:]
        text_list = ""
        for a_elem in a_list:
            text_list += "\n" + a_elem
        with open(a_path, "w") as target_file:
            target_file.write(line_set)
            target_file.write(text_list)

    def process_line(self, line, n_line):
        localizator = str(n_line) + self._localizator_mark
        try:
            pieces = line.split(_FIELD_SEPARATOR)
            if len(pieces) <= 2:
                self._process_error(line=line, localization=localizator, message='Not enough #### found')
                return
            flags = pieces[_FLAGS_INDEX].replace("r", "")
            if 'a' in flags:
                pieces[_FLAGS_INDEX] = flags.replace('a', "")
                self._artist_processor.process_line(_FIELD_SEPARATOR.join(pieces), localizator)
            elif 'm' in flags:
                self._process_modified(original=pieces[_QUERY_INDEX],
                                       modified=pieces[_MODIFIED_CONTENT_INDEX],
                                       flags=flags,
                                       comment="" if len(pieces) < 4 else pieces[_MODIFIED_COMMENT_INDEX],
                                       localization=localizator)
            elif 'c' in flags:
                self._process_clean(content=pieces[_QUERY_INDEX],
                                    comment=pieces[_COMMENT_INDEX],
                                    localization=localizator)
            elif 'd' in flags:
                self._process_discarded(content=pieces[_QUERY_INDEX],
                                        comment=pieces[_COMMENT_INDEX],
                                        localization=localizator)
            elif 'n' in flags:
                if '+' in flags:
                    self._process_mixed(content=pieces[_QUERY_INDEX],
                                        comment=pieces[_COMMENT_INDEX],
                                        localization=localizator)
                else:
                    self._process_noisy(content=pieces[_QUERY_INDEX],
                                        comment=pieces[_COMMENT_INDEX],
                                        localization=localizator)
            else:
                self._process_error(line=line, localization=localizator, message='Unknown flags')

        except BaseException as e:
            self._process_error(line=line, localization=localizator, message=e.message)


    def _process_clean(self, content, comment, localization):
        self._clean_set.add(content)
        self._clean_lines.append(localization + _RESULT_SEPARATOR + content + _RESULT_SEPARATOR + comment)


    def _process_noisy(self, content, comment, localization):
        self._noisy_set.add(content)
        self._noisy_lines.append(localization + _RESULT_SEPARATOR + content + _RESULT_SEPARATOR + comment)


    def _process_mixed(self, content, comment, localization):
        self._mixed_set.add(content)
        self._mixed_lines.append(localization + _RESULT_SEPARATOR + content + _RESULT_SEPARATOR + comment)


    def _process_discarded(self, content, comment, localization):
        self._discarded_lines.append(localization + _RESULT_SEPARATOR + content + _RESULT_SEPARATOR + comment)


    def _process_modified(self, original, modified, flags, comment, localization):
        if 't' in flags:
            self._process_tabbed(original, modified, flags, comment, localization)
        elif 'c' in flags:
            self._clean_set.add(modified)
            self._clean_lines.append(
                localization + _RESULT_SEPARATOR + original + " --> " + modified + _RESULT_SEPARATOR + comment)
        elif 'n' in flags:
            if '+' in flags:
                self._mixed_set.add(modified)
                self._noisy_lines.append(
                    localization + _RESULT_SEPARATOR + original + " --> " + modified + _RESULT_SEPARATOR + comment)
            else:
                self._noisy_set.add(modified)
                self._noisy_lines.append(
                    localization + _RESULT_SEPARATOR + original + " --> " + modified + _RESULT_SEPARATOR + comment)


    def _process_tabbed(self, original, modified, flags, comment, localization):
        if _ENTITY_SEPARATOR not in modified:
            self._process_error(line=original + '#' + flags + '# --> ' + modified, localization=localization,
                                message='Not tabbed')
            return
        entities = modified.split(_ENTITY_SEPARATOR)
        if len(entities) != len(flags) - 2:  # marcas de b(bad) y g(good) menos marcas de m(odified) y t(abbed)
            self._process_error(line=original + '#' + flags + '# --> ' + modified, localization=localization,
                                message='Different number of tabs and flags')
            return
        for i in range(0, len(entities)):
            if flags[i + 2] == 'b':  # bad
                self._noisy_set.add(entities[i])
                self._noisy_lines.append(
                    localization + _RESULT_SEPARATOR + original + " --> " +
                    entities[i] + _RESULT_SEPARATOR + comment + "(from tabbed)")
            elif flags[i + 2] == 'g':  # good
                self._clean_set.add(entities[i])
                self._clean_lines.append(
                    localization + _RESULT_SEPARATOR + original + " --> " +
                    entities[i] + _RESULT_SEPARATOR + comment + "(from tabbed)")
            else:
                self._process_error(line=original + '#' + flags + '# --> ' + entities[i], localization=localization,
                                    message='Unknown tabbed flag')


    def _process_error(self, line, localization, message):
        self._errors.append(localization + _RESULT_SEPARATOR + line + _RESULT_SEPARATOR + message)


# ##########################3


artist_proc = LineProcessor(path_source="original/supervised_extracted_artist.txt",
                            path_clean='clean/clean_artist.txt',
                            path_noisy='noisy/noisy_artist.txt',
                            path_discarded='discarded/discarded_artist.txt',
                            path_mixed='mixed/mixed_artist.txt',
                            path_error='error/error_artist.txt',
                            localizator_mark='a')

song_proc = LineProcessor(path_source="original/supervised_extracted_songs.txt",
                          path_clean='clean/clean_song.txt',
                          path_noisy='noisy/noisy_song.txt',
                          path_discarded='discarded/discarded_song.txt',
                          path_mixed='mixed/mixed_song.txt',
                          path_error='error/error_song.txt',
                          artist_processor=artist_proc,
                          localizator_mark='s')

artist_proc.run()
song_proc.run()
print "Artist: "
artist_proc.save_content()
print "Song:"
song_proc.save_content()



