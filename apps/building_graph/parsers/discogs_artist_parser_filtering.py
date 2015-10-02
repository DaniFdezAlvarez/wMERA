__author__ = 'Dani'

try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree

from wmera.parsers.discogs.artist_parser import DiscogsArtistParser


class DiscogsArtistParserFiltering(DiscogsArtistParser):


    def __init__(self, file_path, dataset, target_ids):
        super(DiscogsArtistParserFiltering, self).__init__(file_path, dataset)
        self._target_ids = target_ids

    def parse_artists(self):
        """
        Return just the artist which an id included in self._target_ids
        :return:
        """
        count_success = 0
        count_done = 0
        for event, elem in ETree.iterparse(self._file_path):  # If no events att specified, only "end" events notified
            if event == 'end':
                if elem.tag == 'artist':
                    artist = self._produce_model_artist(elem)
                    count_done += 1
                    if artist.discogs_id in self._target_ids:
                        count_success += 1
                        yield artist
                        if count_success == len(self._target_ids):
                            break
                    if count_done % 1000 == 0:
                        print "Llevo", count_done
                    elem.clear()
            else:
                print "A non-end??"
