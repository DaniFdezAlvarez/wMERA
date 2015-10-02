from wmera.parsers.discogs.parser_utils import normalize_discogs_name, map_discogs_role

__author__ = 'Dani'

from apps.building_graph.parsers.discogs_song_parser_filtering import DiscogsSongParserFiltering
from wmera.parsers.discogs.song_parser import SONGS, ATTR_RELEASE_ID, TRACK_POSITION, EMPTY_CONTENT, \
    SONG_TITLE, ARTISTS, COLLABORATIONS, ARTIST_NAME, ARTIST_DISCOGS_ID, ARTIST_NAMES_TO_IGNORE, ARTIST_ROLE
from wmera.parsers.discogs.song_parser import DiscogsSongParser
from wmera.mera_core.model.entities import Song, Artist, Collaboration, ROLE_FEATURER


_NODES_TO_PROCESS = [SONGS, ARTISTS, COLLABORATIONS]


class DiscogsSongParserFilteringNoNamevars(DiscogsSongParserFiltering):
    def __init__(self, file_path, dataset, target_indexes, target_ids):
        super(DiscogsSongParserFilteringNoNamevars, self).__init__(file_path, dataset, target_indexes, target_ids)


    @staticmethod
    def _produce_model_songs(elem):
        """
        It yields as many songs as tracks can be found in the received elem.

        """
        nodes_to_process = {}
        for subnode in list(elem):
            if subnode.tag in _NODES_TO_PROCESS:
                nodes_to_process[subnode.tag] = subnode

        for song in DiscogsSongParserFilteringNoNamevars._process_nodes(nodes_to_process, elem.attrib[ATTR_RELEASE_ID]):
            yield song


    @staticmethod
    def _process_nodes(nodes_to_process, release_id):

        list_of_artist = []
        list_of_collaborations = []

        if ARTISTS in nodes_to_process:
            for artist in DiscogsSongParserFilteringNoNamevars._process_artists_node(nodes_to_process[ARTISTS]):
                list_of_artist.append(artist)

        if COLLABORATIONS in nodes_to_process:
            for collaboration in DiscogsSongParserFilteringNoNamevars._process_collaborations_node(nodes_to_process[COLLABORATIONS]):
                if collaboration[0] == ROLE_FEATURER:
                    list_of_artist.append(collaboration[1])
                else:
                    list_of_collaborations.append(collaboration[1])


        for song in DiscogsSongParserFilteringNoNamevars \
                ._process_songs_node(songs_node=nodes_to_process[SONGS],
                                     artists=list_of_artist,
                                     collaborations=list_of_collaborations,
                                     album=None,
                                     genres=None,
                                     country=None,
                                     release_date=None,
                                     release_id=release_id):
            yield song


    @staticmethod
    def _process_collaborations_node(collaborations_node):
        for artist_node in list(collaborations_node):
            name = None
            roles = []
            discogs_id = None
            for elem in list(artist_node):
                if elem.tag == ARTIST_NAME:
                    name = normalize_discogs_name(elem.text)
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
                                                     discogs_id=discogs_id))
                    elif role in Collaboration.valid_roles():
                        yield (role, Collaboration(collaborator=Artist(canonical=name,  # Returning a tuple
                                                                       discogs_id=discogs_id),
                                                   role=role))


    @staticmethod
    def _process_artists_node(artists_node):
        for artist_node in list(artists_node):
            name = None
            discogs_id = None
            for elem in list(artist_node):
                if elem.tag == ARTIST_NAME:
                    name = normalize_discogs_name(elem.text)
                elif elem.tag == ARTIST_DISCOGS_ID:
                    discogs_id = int(elem.text)
            if name is not None and name not in ARTIST_NAMES_TO_IGNORE:
                yield Artist(canonical=name,
                             discogs_id=discogs_id)



    @staticmethod
    def _process_songs_node(songs_node, artists, collaborations, album, genres, country, release_date, release_id):
        for song_node in list(songs_node):
            title = None
            discogs_id = None
            extra_collaborations = []
            for elem in list(song_node):
                if elem.tag == SONG_TITLE:
                    title = normalize_discogs_name(elem.text)
                elif elem.tag == TRACK_POSITION:
                    discogs_id = DiscogsSongParser.build_discogs_id(release_id, elem.text)
                elif elem.tag == COLLABORATIONS:
                    for a_coll in DiscogsSongParserFilteringNoNamevars._process_collaborations_node(elem):
                        if a_coll[0] == ROLE_FEATURER:
                            artists.append(a_coll[1])
                        else:
                            extra_collaborations.append(a_coll[1])
            if title not in EMPTY_CONTENT:
                yield Song(canonical=title,
                           discogs_id=discogs_id,
                           artists=artists,
                           collaborations=collaborations)