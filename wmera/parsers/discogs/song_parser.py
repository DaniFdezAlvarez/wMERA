from wmera.mera_core.str_ops.normalization import remove_brackets_info

__author__ = 'Dani'

from wmera.parsers.interface.song_parser_interface import SongParserInterface
from wmera.parsers.discogs.parser_utils import normalize_discogs_name, map_discogs_role, \
    get_subnodes_text, EMPTY_CONTENT
from wmera.mera_core.model.entities import Song, Artist, Collaboration, ROLE_FEATURER

try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree

ARTISTS = "artists"
ALBUM = "title"
COLLABORATIONS = "extraartists"
GENRES = "genres"
STYLES = "styles"
COUNTRY = "country"
RELEASE_DATE = "released"
SONGS = "tracklist"

ARTIST_NAME = "name"
ARTIST_NAMEVAR = "anv"
ARTIST_ROLE = "role"
ARTIST_DISCOGS_ID = "id"

SONG_TITLE = "title"
SONG_DURATION = "duration"

ATTR_RELEASE_ID = "id"
TRACK_POSITION = "position"

_NODES_TO_PROCESS = [ARTISTS, ALBUM, COLLABORATIONS, GENRES, STYLES, COUNTRY, RELEASE_DATE, SONGS]

ARTIST_NAMES_TO_IGNORE = ["Various", "Traditional"]


class DiscogsSongParser(SongParserInterface):
    def __init__(self, file_path, dataset):
        super(DiscogsSongParser, self).__init__(dataset)
        self._file_path = file_path


    def parse_songs(self):
        """
        Yield as many Songs as tracks in releases can be found in the content pointed
        by file_path

        Generator.
        :return:
        """
        for event, elem in ETree.iterparse(self._file_path):  # If no events att specified, only "end" events notified
            if event == 'end':
                if elem.tag == 'release':
                    for song in self._produce_model_songs(elem):
                        yield song
                    elem.clear()
            else:
                print "A non-end??"


    @staticmethod
    def _produce_model_songs(elem):
        """
        It yields as many songs as tracks can be found in the received elem.

        """
        nodes_to_process = {}
        for subnode in list(elem):
            if subnode.tag in _NODES_TO_PROCESS:
                nodes_to_process[subnode.tag] = subnode

        for song in DiscogsSongParser._process_nodes(nodes_to_process, elem.attrib[ATTR_RELEASE_ID]):
            yield song


    @staticmethod
    def _process_nodes(nodes_to_process, release_id):
        list_of_artist = []
        list_of_collaborations = []
        album = None
        list_of_genres = set()
        country = None
        release_date = None

        if ARTISTS in nodes_to_process:
            for artist in DiscogsSongParser._process_artists_node(nodes_to_process[ARTISTS]):
                list_of_artist.append(artist)

        if ALBUM in nodes_to_process:
            album = DiscogsSongParser._process_album_node(nodes_to_process[ALBUM])

        if COLLABORATIONS in nodes_to_process:
            for collaboration in DiscogsSongParser._process_collaborations_node(nodes_to_process[COLLABORATIONS]):
                if collaboration[0] == ROLE_FEATURER:
                    list_of_artist.append(collaboration[1])
                else:
                    list_of_collaborations.append(collaboration[1])

        if GENRES in nodes_to_process:
            for genre in DiscogsSongParser._process_genres_node(nodes_to_process[GENRES]):
                list_of_genres.add(genre)

        if STYLES in nodes_to_process:
            for style in DiscogsSongParser._process_styles_node(nodes_to_process[STYLES]):
                list_of_genres.add(style)

        if COUNTRY in nodes_to_process:
            country = DiscogsSongParser._process_country_node(nodes_to_process[COUNTRY])

        if release_date in nodes_to_process:
            release_date = DiscogsSongParser._process_date_node(nodes_to_process[RELEASE_DATE])

        for song in DiscogsSongParser._process_songs_node(songs_node=nodes_to_process[SONGS],
                                                          artists=list_of_artist,
                                                          collaborations=list_of_collaborations,
                                                          album=album,
                                                          genres=list_of_genres,
                                                          country=country,
                                                          release_date=release_date,
                                                          release_id=release_id):
            yield song


    @staticmethod
    def _process_artists_node(artists_node):
        for artist_node in list(artists_node):
            name = None
            namevars = []
            discogs_id = None
            for elem in list(artist_node):
                if elem.tag == ARTIST_NAME:
                    name = normalize_discogs_name(elem.text)
                elif elem.tag == ARTIST_NAMEVAR:
                    candidate_namevar = normalize_discogs_name(elem.text)
                    if candidate_namevar is not None:
                        namevars.append(candidate_namevar)
                elif elem.tag == ARTIST_DISCOGS_ID:
                    discogs_id = int(elem.text)
            if name is not None and name not in ARTIST_NAMES_TO_IGNORE:
                yield Artist(canonical=name,
                             namevars=namevars,
                             discogs_id=discogs_id)

    @staticmethod
    def _process_album_node(album_node):
        return normalize_discogs_name(album_node.text)

    @staticmethod
    def _process_collaborations_node(collaborations_node):
        for artist_node in list(collaborations_node):
            name = None
            namevars = []
            roles = []
            discogs_id = None
            for elem in list(artist_node):
                if elem.tag == ARTIST_NAME:
                    name = normalize_discogs_name(elem.text)
                elif elem.tag == ARTIST_NAMEVAR:
                    namevars.append(normalize_discogs_name(elem.tag))
                elif elem.tag == ARTIST_ROLE:
                    for role in elem.text.split(","):
                        candidate_r = map_discogs_role(role.strip())
                        if candidate_r is not None:
                            roles.append(candidate_r)
                elif elem.tag == ARTIST_DISCOGS_ID:
                    discogs_id = int(elem.text)
            if name is not None:
                for role in roles:
                    if role == ROLE_FEATURER:
                        yield (ROLE_FEATURER, Artist(canonical=name,  # Returning a tuple
                                                     namevars=namevars,
                                                     discogs_id=discogs_id))
                    elif role in Collaboration.valid_roles():
                        yield (role, Collaboration(collaborator=Artist(canonical=name,  # Returning a tuple
                                                                       namevars=namevars,
                                                                       discogs_id=discogs_id),
                                                   role=role))

    @staticmethod
    def _process_genres_node(genres_node):
        for genre in get_subnodes_text(genres_node):
            yield genre


    @staticmethod
    def _process_styles_node(styles_node):
        for style in get_subnodes_text(styles_node):
            yield style

    @staticmethod
    def _process_country_node(country_node):
        country_text = normalize_discogs_name(country_node.text)
        if country_text not in EMPTY_CONTENT:
            return country_text
        else:
            return None

    @staticmethod
    def _process_date_node(date_node):
        # TODO revise when refining dates
        date_text = date_node.text.strip()
        if date_text not in EMPTY_CONTENT:
            return date_text
        else:
            return None


    @staticmethod
    def build_discogs_id(release_id, track_position):
        return "[r" + release_id + "]" + track_position if track_position is not None else "[r" + release_id + "]"


    @staticmethod
    def _process_songs_node(songs_node, artists, collaborations, album, genres, country, release_date, release_id):
        for song_node in list(songs_node):
            title = None
            alt_titles = None
            duration = None
            discogs_id = None
            extra_collaborations = []
            for elem in list(song_node):
                if elem.tag == SONG_TITLE:
                    title = normalize_discogs_name(elem.text)

                elif elem.tag == SONG_DURATION:
                    duration = DiscogsSongParser._parse_duration(elem.text)
                elif elem.tag == COLLABORATIONS:
                    for a_coll in DiscogsSongParser._process_collaborations_node(elem):
                        if a_coll[0] == ROLE_FEATURER:
                            artists.append(a_coll[1])
                        else:
                            extra_collaborations.append(a_coll[1])
                elif elem.tag == TRACK_POSITION:
                    discogs_id = DiscogsSongParser.build_discogs_id(release_id, elem.text)
            if title not in EMPTY_CONTENT:
                candidate_alt_title = remove_brackets_info(title)
                if title != candidate_alt_title:
                    alt_titles = [candidate_alt_title]
                yield Song(canonical=title,
                           artists=artists,
                           alt_titles=alt_titles,
                           collaborations=collaborations + extra_collaborations,
                           duration=duration,
                           genres=genres,
                           release_date=release_date,
                           album=album,
                           country=country,
                           discogs_id=discogs_id)

    @staticmethod
    def _parse_duration(duration):
        if duration in EMPTY_CONTENT:
            return None
        duration = duration.strip().split(":")
        if len(duration) != 2:
            return None
        return int(duration[0]) * 60 + int(duration[1])



