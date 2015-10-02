__author__ = 'Dani'

try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree

from test.useful_code.tsv_adapter.model.discogs_entities import Artist


NAME = 'name'
REAL_NAME = 'realname'
NAME_VARIATIONS = 'namevariations'
ALIASES = 'aliases'
MEMBERS = 'members'
DATA_QUALITY = 'data_quality'


class DiscogsArtistParser(object):

    def __init__(self, file_path):
        self._file_path = file_path


    def parse_artist(self):
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

        return DiscogsArtistParser._process_nodes(nodes_to_process)


    @staticmethod
    def _process_nodes(nodes_to_process):
        result = Artist(None)
        # name
        result.name = nodes_to_process[NAME].text
        # data_quality
        result.data_quality = nodes_to_process[DATA_QUALITY].text
        #real_name
        if 'members' in nodes_to_process:
            DiscogsArtistParser._process_members_node(result, nodes_to_process[MEMBERS])
        elif REAL_NAME in nodes_to_process:
            result.add_real_name(nodes_to_process[REAL_NAME].text)
        #namevariations
        if NAME_VARIATIONS in nodes_to_process:
            DiscogsArtistParser._process_namevariations_node(result, nodes_to_process[NAME_VARIATIONS])
        #aliases
        if ALIASES in nodes_to_process:
            DiscogsArtistParser._process_aliases_node(result, nodes_to_process[ALIASES])
        return result


    @staticmethod
    def _process_namevariations_node(artist_obj, node):
        for name_variation in DiscogsArtistParser._get_subnode_names(node):
            artist_obj.add_name_variation(name_variation)

    @staticmethod
    def _process_aliases_node(artist_obj, node):
        for alias in DiscogsArtistParser._get_subnode_names(node):
            artist_obj.add_alias(alias)

    @staticmethod
    def _process_members_node(artist_obj, node):
        for real_name in DiscogsArtistParser._get_subnode_names(node):
            artist_obj.add_real_name(real_name)

    @staticmethod
    def _get_subnode_names(node):
        for elem in list(node):
            if elem.text is not None:
                yield elem.text


