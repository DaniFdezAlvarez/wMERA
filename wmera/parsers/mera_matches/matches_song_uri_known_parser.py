__author__ = 'Dani'

from wmera.parsers.interface.song_parser_uri_known_interface import SongParserUriKnownInterface
from wmera.utils import decode_dict
from wmera.mera_core.model.entities import Song, Artist, ROLE_WRITER, Collaboration
from rdflib import URIRef
import json

SONG_NAME = "query"
ISWC = "iswc"
REFINEMENTS = "refinements"
REF_TYPE = "type"
REF_CONTENT = "content"
RESULTS = "results"
URI_RESULT = "entity"

TYPE_ARTIST = "artist"
TYPE_WRITER = "writer"


class MatchesSongUriKnownParser(SongParserUriKnownInterface):


    def __init__(self, dataset, json_string):
        super(MatchesSongUriKnownParser, self).__init__(dataset)
        self._json_string = json_string

    def parse_songs(self):
        json_content = json.loads(self._json_string, object_hook=decode_dict)
        for a_dict in json_content:
            result = Song(canonical=a_dict[SONG_NAME],
                          iswc=a_dict[ISWC])
            for refinements_dict in a_dict[REFINEMENTS]:
                if refinements_dict[REF_TYPE] == TYPE_ARTIST:
                    result.add_artist(Artist(canonical=refinements_dict[REF_CONTENT]))
                elif refinements_dict[REF_TYPE] == TYPE_WRITER:
                    result.add_collaboration(Collaboration(collaborator=Artist(canonical=refinements_dict[REF_CONTENT]),
                                                           role=ROLE_WRITER))
            # print "____________"
            for a_result_dict in a_dict[RESULTS]:
                # print (URIRef(a_result_dict[URI_RESULT]), result.canonical)
                yield (URIRef(a_result_dict[URI_RESULT]), result)
            # print "____________"







