__author__ = 'Dani'

from wmera.parsers.discogs.song_parser import DiscogsSongParser
try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree



class DiscogsSongParserFiltering(DiscogsSongParser):
    """
    Only yields song with index in target_index
    """
    def __init__(self, file_path, dataset, target_indexes, target_ids):
        super(DiscogsSongParserFiltering, self).__init__(file_path, dataset)
        self._target_indexes = target_indexes
        self._target_ids = target_ids



    def parse_songs(self):
        """
        Yield as many Songs as tracks in releases can be found in the content pointed
        by file_path

        Generator.
        :return:
        """

        index_count = 0
        success_count = 0

        for event, elem in ETree.iterparse(self._file_path):  # If no events att specified, only "end" events notified
            if event == 'end':
                if elem.tag == 'release':
                    for song in self._produce_model_songs(elem):
                        index_count += 1
                        if index_count in self._target_indexes or song.discogs_id in self._target_ids:
                            success_count += 1
                            yield song
                    if success_count >= len(self._target_indexes):
                        break
                    elem.clear()
            else:
                print "A non-end??"