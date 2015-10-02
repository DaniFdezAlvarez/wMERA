__author__ = 'Dani'


try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree


VALID_ROLES = ["Written-By", "Music By", "Producer", "Vocals", "Feat.", "Featuring"]


class DiscogsSongParserArtistIdDetection(object):


    def extract_artist_ids_from_artists_nodes(self, elem, extra=False):
        result = set()
        if not extra:
            for artist_node in list(elem):
                for subnode in list(artist_node):
                    if subnode.tag == "id":
                        result.add(int(subnode.text))
                        break
        else:
            for artist_node in list(elem):
                id_int = None
                role_text = None
                for subnode in list(artist_node):
                    if subnode.tag == "id":
                        id_int = int(subnode.text)
                    elif subnode.tag == 'role':
                        role_text = subnode.text
                if role_text is not None:
                    for a_valid in VALID_ROLES:
                        if a_valid in role_text:
                            result.add(id_int)


        return result


    def detect_song_artists_ids(self, elem):
        tracklist = None
        artists = None
        extras = None

        for subnode in list(elem):
            if subnode.tag == 'tracklist':
                tracklist = subnode
            elif subnode.tag == 'artists':
                artists = subnode
            elif subnode.tag == 'extraartists':
                extras = subnode

        if tracklist is not None:
            title = None
            common_artists = self.extract_artist_ids_from_artists_nodes(artists)
            if extras is not None:
                common_artists = self.extract_artist_ids_from_artists_nodes(extras, True).union(common_artists)
            for track in list(tracklist):
                extraartist_track_node = None
                for track_node in list(track):
                    if track_node.tag == 'extraartists':
                        extraartist_track_node = track_node
                        break
                    if track_node.tag == 'title':
                        title = track_node.text
                if extraartist_track_node is not None:
                    yield title, common_artists.union(self.extract_artist_ids_from_artists_nodes(extraartist_track_node, True))
                else:
                    yield title, common_artists

    def run(self, file_path, target_discogs_indexes):
        result = set()
        index_count = 0
        for event, elem in ETree.iterparse(file_path):
            if event == 'end':
                if elem.tag == 'release':
                    for title, artists_set in self.detect_song_artists_ids(elem):
                        index_count += 1
                        if index_count % 100000 == 0:
                            print "Hechas ", index_count
                        if index_count in target_discogs_indexes:
                            for artist_id in artists_set:
                                result.add(artist_id)
                            #     print "Eh!", artist_id
                            # print "----"
                        # if title == "New World Order (Dr. Rhythm's Trance Hop Mix)":
                        #     print index_count, "NEW WORLD ORDER"
                        # if title == "Giv Me Luv (Deep Dish 11th Hour Remix)":
                        #     print index_count, "GIV ME LUV"
                        # if title == "Exploration Of Space (DJ Shredda Remix)":
                        #     print index_count, "EXPLORATION OF SPACE"
                        # if title is not None and "Holding On To Nothing" in title:
                        #     print index_count, "HOLDING ON"
                    elem.clear()
        return result