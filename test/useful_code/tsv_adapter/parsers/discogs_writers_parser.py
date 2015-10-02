__author__ = 'Dani'

import re

try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree

from test.useful_code.tsv_adapter.model.discogs_entities import Artist


NAME = 'name'
EXTRAARTIST = 'extraartists'
ARTIST = "artist"
ROLE = 'role'
WRITTER = 'Written-By'
ROLE_SEPARATOR = ','
DATA_QUALITY = 'data_quality'

BRACKETS_PATTERN = re.compile("\([0-9]+\)")
EXTRA_ROLE_INFO_PATTERN = re.compile("\[.*\]")


class DiscogsWriterParser(object):

    def __init__(self, file_path):
        self._file_path = file_path


    def parse_artist(self):
        """
        Return as many DiscogArtist as writers can be found in the received xml file.
        Generator.
        :return:
        """
        for event, elem in ETree.iterparse(self._file_path):  # If no events att specified, only "end" events notified
            if event == 'end':
                if elem.tag == 'release':
                    candidate_result = self._produce_model_writers(elem)
                    if candidate_result is not None:
                        for writer in candidate_result:
                            yield writer
                    elem.clear()
            else:
                print "A non-end??"


    @staticmethod
    def _produce_model_writers(elem):
        """It returns None if no writers were find within the received node.
        Otherwise, it returns a list containing all the found writers.
        """
        nodes_to_process = {}
        for subnode in list(elem):
            if subnode.tag == EXTRAARTIST:
                nodes_to_process[EXTRAARTIST] = subnode
            elif subnode.tag == DATA_QUALITY:
                nodes_to_process[DATA_QUALITY] = subnode


        return DiscogsWriterParser._process_nodes(nodes_to_process)


    @staticmethod
    def _process_nodes(nodes_to_process):
        if EXTRAARTIST not in nodes_to_process:
            return None

        # data_quality
        data_quality = nodes_to_process[DATA_QUALITY].text

        #names and real_names
        names = DiscogsWriterParser._look_for_writer_names(nodes_to_process[EXTRAARTIST])
        if len(names) == 0:
            return None
        else:
            result = []
            for name in names:
                result.append(Artist(name=name, real_name=[name], data_quality=data_quality))
            return result


    @staticmethod
    def _look_for_writer_names(extraartist_node):
        result = []

        for artist in list(extraartist_node):
            writer_name = DiscogsWriterParser._get_writer_name_from_artist_node_if_exist(artist)
            if writer_name != "":
                result.append(writer_name)
        return result


    @staticmethod
    def _get_writer_name_from_artist_node_if_exist(artist_node):
        name, roles = None, None
        for subnode in list(artist_node):
            if subnode.tag == NAME:
                name = BRACKETS_PATTERN.sub("", subnode.text).strip()
            elif subnode.tag == ROLE:
                roles = DiscogsWriterParser._extract_roles_from_string(subnode.text)

        if WRITTER in roles:
            return name

    @staticmethod
    def _extract_roles_from_string(original_str):
        roles = original_str.split(",")
        for i in range(0, len(roles)):
            roles[i] = EXTRA_ROLE_INFO_PATTERN.sub("", roles[i]).strip()
        return roles







