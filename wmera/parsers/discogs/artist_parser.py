__author__ = 'Dani'

from wmera.parsers.interface.artist_parser_interface import ArtistParserInterface
from wmera.parsers.discogs.parser_utils import normalize_discogs_name, get_subnodes_text


try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree

from wmera.mera_core.model.entities import ArtistPerson, ArtistGroup


NAME = 'name'
REAL_NAME = 'realname'
NAME_VARIATIONS = 'namevariations'
ALIASES = 'aliases'
MEMBERS = 'members'
DATA_QUALITY = 'data_quality'
DISCOGS_ID = "id"

correct_arr = ["Correct", "correct", "Complete and Correct"]


class DiscogsArtistParser(ArtistParserInterface):

    def __init__(self, file_path, dataset):
        super(DiscogsArtistParser, self).__init__(dataset)
        self._file_path = file_path


    def parse_artists(self):
        """
        Return as many DiscogArtist as discogs nodes can be found in the received file.
        Generator.
        :return:
        """
        for event, elem in ETree.iterparse(self._file_path):  # If no events att specified, only "end" events notified
            if event == 'end':
                if elem.tag == 'artist':
                    yield self._produce_model_artist(elem)
                    elem.clear()
            else:
                print "A non-end??"


    @staticmethod
    def _produce_model_artist(elem):
        nodes_to_process = {}
        for subnode in list(elem):
            if subnode.tag == NAME:
                nodes_to_process[NAME] = subnode
            elif subnode.tag == REAL_NAME:
                nodes_to_process[REAL_NAME] = subnode
            elif subnode.tag == DATA_QUALITY:
                nodes_to_process[DATA_QUALITY] = subnode
            elif subnode.tag == NAME_VARIATIONS:
                nodes_to_process[NAME_VARIATIONS] = subnode
            elif subnode.tag == ALIASES:
                nodes_to_process[ALIASES] = subnode
            elif subnode.tag == MEMBERS:
                nodes_to_process[MEMBERS] = subnode
            elif subnode.tag == DISCOGS_ID:
                nodes_to_process[DISCOGS_ID] = subnode

        return DiscogsArtistParser._process_nodes(nodes_to_process)


    @staticmethod
    def _process_nodes(nodes_to_process):

        # ##Filtering quality  # NOT NEEDED
        # data_quality = nodes_to_process[DATA_QUALITY].text
        # if data_quality not in correct_arr:
        #     return None  # TODO: decide what to do... in the future ;)

        ## If there are members, it is a group.
        if MEMBERS in nodes_to_process:
            return DiscogsArtistParser._process_nodes_of_group(nodes_to_process)
        else:
            return DiscogsArtistParser._process_nodes_of_person(nodes_to_process)



    @staticmethod
    def _process_nodes_of_group(nodes_to_process):
        # canonical
        canonical = normalize_discogs_name(nodes_to_process[NAME].text)
        #discogs_id
        discogs_id = int(nodes_to_process[DISCOGS_ID].text)

        #Declaring artist result
        result = ArtistGroup(canonical=canonical, discogs_id=discogs_id)

        #namevariations
        if NAME_VARIATIONS in nodes_to_process:
            DiscogsArtistParser._process_namevariations_node(result, nodes_to_process[NAME_VARIATIONS])

        #aliases
        if ALIASES in nodes_to_process:
            DiscogsArtistParser._process_aliases_node(result, nodes_to_process[ALIASES])

        # MEMBER . This node should be present, no need to check. It is the way we have
        # to distinguish between single artists and groups
        DiscogsArtistParser._process_members_node(result, nodes_to_process[MEMBERS])


        return result


    @staticmethod
    def _process_nodes_of_person(nodes_to_process):
        # canonical
        canonical = normalize_discogs_name(nodes_to_process[NAME].text)

        #discogs_id
        discogs_id = int(nodes_to_process[DISCOGS_ID].text)

        #civil
        civil = None
        if REAL_NAME in nodes_to_process:
            civil = normalize_discogs_name(nodes_to_process[REAL_NAME].text)

        #Declaring artist result
        result = ArtistPerson(canonical=canonical, civil=civil, discogs_id=discogs_id)

        #namevariations
        if NAME_VARIATIONS in nodes_to_process:
            DiscogsArtistParser._process_namevariations_node(result, nodes_to_process[NAME_VARIATIONS])

        #aliases
        if ALIASES in nodes_to_process:
            DiscogsArtistParser._process_aliases_node(result, nodes_to_process[ALIASES])

        return result


    @staticmethod
    def _process_namevariations_node(artist_obj, node):
        for name_variation in get_subnodes_text(node):
            artist_obj.add_namevar(name_variation)


    @staticmethod
    def _process_aliases_node(artist_obj, node):
        for alias in get_subnodes_text(node):
            artist_obj.add_alias(alias)


    @staticmethod
    def _process_members_node(group_obj, node):
        for member_name in get_subnodes_text(node):
            group_obj.add_member(ArtistPerson(canonical=member_name))





