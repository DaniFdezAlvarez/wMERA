from wmera.parsers.discogs.parser_utils import normalize_discogs_name

__author__ = 'Dani'

from apps.building_graph.parsers.discogs_artist_parser_filtering import DiscogsArtistParserFiltering
from wmera.parsers.discogs.artist_parser import NAME, DISCOGS_ID
from wmera.mera_core.model.entities import Artist


class DiscogsArtistParserFilteringNoNamevars(DiscogsArtistParserFiltering):


    def __init__(self, file_path, dataset, target_ids):
        super(DiscogsArtistParserFilteringNoNamevars, self).__init__(file_path, dataset, target_ids)


    @staticmethod
    def _produce_model_artist(elem):
        nodes_to_process = {}
        for subnode in list(elem):
            if subnode.tag == NAME:
                nodes_to_process[NAME] = subnode
            elif subnode.tag == DISCOGS_ID:
                nodes_to_process[DISCOGS_ID] = subnode

        return DiscogsArtistParserFilteringNoNamevars._process_nodes(nodes_to_process)


    @staticmethod
    def _process_nodes(nodes_to_process):
        # canonical
        canonical = normalize_discogs_name(nodes_to_process[NAME].text)

        #discogs_id
        discogs_id = int(nodes_to_process[DISCOGS_ID].text)


        #Declaring artist result
        return Artist(canonical=canonical, discogs_id=discogs_id)

