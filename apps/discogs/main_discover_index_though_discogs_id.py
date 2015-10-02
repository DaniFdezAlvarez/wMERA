__author__ = 'Dani'

try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree



def process_raw_discogs_id(raw_id):
    """
    FORMAT EXPECTED:    [rXXXXXX]str_position
    :param raw_id:
    :return: tuple (ID_RECORDING, POSITION), both strings
    """
    separator_index = raw_id.index("]")
    return raw_id[2:separator_index], raw_id[separator_index + 1:]



def read_target_aol_ids(file_path):
    first_line = True
    result = set()
    with open(file_path, "r") as file_io:
            for line in file_io:
                if first_line:
                    first_line = False
                else:
                    line = line.replace("\n", "")
                    if line != "":
                        result.add(process_raw_discogs_id(line.split("\t")[-1]))
    return result


def read_target_musicbrainz_ids(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        file_io.readline()
        for line in file_io:
            line = line.replace("\n", "")
            if line != "":
                result.add(process_raw_discogs_id(line.split("\t")[1]))
    return result


def extract_releases_ids(target_set_tuples):
    result = set()
    for elem in target_set_tuples:
        result.add(elem[0])
    return result


def detect_song_id(elem):
    release_id = elem.attrib["id"]
    tracklist = None
    for subnode in list(elem):
        if subnode.tag == 'tracklist':
            tracklist = subnode
            break
    if tracklist is not None:
        for track in list(tracklist):
            track_id_node = None
            for track_node in list(track):
                if track_node.tag == 'position':
                    track_id_node = track_node
                    break
            yield release_id, track_id_node.text




def locate_index_of_ids(file_path, discogs_complete_ids, discogs_releases_ids):
    result = set()
    index_count = 0
    for event, elem in ETree.iterparse(file_path):
        if event == 'end':
            if elem.tag == 'release':
                for song in detect_song_id(elem):
                    index_count += 1
                    if index_count % 100000 == 0:
                        print "Hechas ", index_count
                    if song[0] in discogs_releases_ids and song in discogs_complete_ids:
                        print "Found One! ", song
                        result.add(index_count)
                elem.clear()
    return result




##################   Program   #####################


set_tuples_aol_ids = read_target_aol_ids("files/random_final_queries_without_discarded.txt")
set_tuples_mbrainz_ids = read_target_musicbrainz_ids("files/random_musicbrainz.tsv")
set_songs = set_tuples_aol_ids.union(set_tuples_mbrainz_ids)
set_releases_ids = extract_releases_ids(set_songs)

index_of_ids = locate_index_of_ids("../../files/discogs_releases.xml", set_songs, set_releases_ids)

with open("files/aol_discogs_indexes.txt", "w") as file_io:
    for index in index_of_ids:
        file_io.write(str(index) + "\n")




