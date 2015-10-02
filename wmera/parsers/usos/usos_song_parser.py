from wmera.parsers.interface.song_parser_interface import SongParserInterface
from wmera.mera_core.model.entities import Song, Artist, Collaboration, ROLE_WRITER

__author__ = 'Dani'


_FEAT_VARS = [" feat ", " feat. ", " featuring ", " ft ", " ft. "]


class UsosSongParser(SongParserInterface):


    def __init__(self, dataset, source_file):
        super(UsosSongParser, self).__init__(dataset)
        self._source_file = source_file


    def parse_songs(self):
        with open(self._source_file, 'r') as in_file:
            in_file.readline()  # We must discard the first line (headers)
            for line in in_file:
                candidate_song = self._build_song_from_line(line)
                if candidate_song is not None:
                    yield candidate_song


    def _build_song_from_line(self, line):
        parts = line.replace("\n", "").replace("\r", "").split("\t")
        if len(parts) < 3:
            return None


        list_of_artists = self._process_artists(parts[1])
        if list_of_artists is None:
            return None

        title = self._process_title(parts[2])
        if title is None:
            return None

        transaction_id = self._process_transaction_id(parts[0])


        isrc = None
        if len(parts) > 3:
            isrc = self._process_isrc(parts[3])

        album = None
        list_of_creators = None

        ## The line should have, at least, identifier, artist and song. If not, it is not valid.
        ## In the originla file all the lines has 6 "\t", so it should be possible to split every
        ## line in 7 parts. But when the line ends with one or more "\t" char, the python parser
        ## just erase it. That why we should use this conditionals.
        if len(parts) > 3:
            if len(parts) > 4:
                if len(parts) > 5:
                    if len(parts) > 6:
                        album = self._process_album(parts[6])
                    list_of_labels = self._process_labels(parts[5])
                list_of_creators = self._process_creators(parts[4])
            isrc = self._process_isrc(parts[3])

        result = Song(canonical=title,
                      artists=list_of_artists,
                      collaborations=list_of_creators,
                      duration=None,
                      genres=None,
                      release_date=None,
                      album=album,
                      alt_titles=None,
                      country=None,
                      usos_isrc=isrc,
                      usos_transaction_id=transaction_id)
        return result



    @staticmethod
    def _process_transaction_id(original_str):
        try:
            return str(int(original_str.strip()))
        except:
            return None

    @staticmethod
    def _process_isrc(original_str):
        if original_str == "":
            return None
        if " " in original_str:
            return None
        return original_str.strip()

    @staticmethod
    def _process_artists(original_str):
        if original_str.strip() == "":
            return None
        list_of_names = original_str.split("||")
        result = []
        for a_name in list_of_names:
            result.append(Artist(canonical=a_name))
        return result

    @staticmethod
    def _process_title(original_str):
        if original_str.strip() == "":
            return None
        original_str = original_str.lower()
        for a_var in _FEAT_VARS:
            pos = original_str.find(a_var)
            if pos != -1:
                original_str = original_str[:pos]
                break
        return original_str

    @staticmethod
    def _process_isrc(original_str):
        candidate = original_str.strip()
        if candidate == "":
            return None
        else:
            return candidate

    @staticmethod
    def _process_creators(original_str):
        list_of_names = None
        if original_str.strip() == "":
            return None
        if "||" in original_str:
            list_of_names = original_str.split("||")
        else:
            list_of_names = original_str.split(",")
        resutl = []
        for a_name in list_of_names:
            resutl.append(Collaboration(collaborator=Artist(canonical=a_name),
                                        role=ROLE_WRITER))
        return resutl


    @staticmethod
    def _process_labels(original_str):
        if original_str.strip() == "":
            return None
        return original_str.split(",")

    @staticmethod
    def _process_album(original_str):
        if original_str.strip() == "":
            return None
        return original_str









