__author__ = 'Dani'

from apps.building_graph.parsers.discogs_song_parser_artist_id_detection import DiscogsSongParserArtistIdDetection


def read_target_discog_song_indexes(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        for line in file_io:
            result.add(int(line[0:-1]))
    return result



target_discogs_song_indexes = read_target_discog_song_indexes("files/500000_discogs_song_indexes.txt")
# target_discogs_song_indexes = read_target_discog_song_indexes("files/all_discogs_indexes.txt")
artist_indexes = DiscogsSongParserArtistIdDetection().run("../../files/discogs_releases.xml",
                                                          target_discogs_song_indexes)


with open("files/artists_indexes_for_500000_discogs_songs.txt", "w") as file_io:
    for an_index in artist_indexes:
        file_io.write(str(an_index) + "\n")