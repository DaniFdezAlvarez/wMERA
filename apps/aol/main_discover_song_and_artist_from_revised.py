__author__ = 'Dani'

from wmera.utils import rel_path_to_file
from comparator import levenshtein


def persist_set(target_set, file_path):
    result = ""
    for elem in target_set:
        result += elem + "\t"
    result = result[0:-1]
    with open(file_path, "w") as file_io:
        file_io.write(result)



def set_of_words_from_file_separator(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        target_line = file_io.readline()
        if target_line.endswith("\n"):
            target_line = target_line[0:-1]
        names = target_line.split("||")
        for name in names:
            if name.strip() != "":
                result.add(name.strip())

    return result


def list_of_lists_of_words_from_file_lines(file_path):
    result = []
    with open(file_path, "r") as file_io:
        for line in file_io:
            if line.endswith("\n"):
                line = line[0:-1]
            tmp_arr = line.split("\t")
            result.append(tmp_arr)
    return result


def name_included_in_min_levenshtein_distance(name, target_et):
    for elem in target_et:
        if levenshtein(elem, name) <= 1:
            return True
    return False



##################### ------------ Program ----------- #########################

print "Eh que soy yo"

clean_artist = set_of_words_from_file_separator(rel_path_to_file("files/clean_artist.txt",
                                                                 __file__))

noisy_artist = set_of_words_from_file_separator(rel_path_to_file("files/noisy_artist.txt",
                                                                 __file__))

clean_songs = set_of_words_from_file_separator(rel_path_to_file("files/clean_song.txt",
                                                                __file__))

noisy_songs = set_of_words_from_file_separator(rel_path_to_file("files/noisy_song.txt",
                                                                __file__))

artist_parsed = clean_artist.union(noisy_artist)
songs_parsed = clean_songs.union(noisy_songs)

noisy_queries = list_of_lists_of_words_from_file_lines(
    rel_path_to_file("files/noisy-musical-queries.txt",
                     __file__))


final_artist = set().union(artist_parsed)
final_song = set().union(songs_parsed)


for a_noisy_list in noisy_queries:
    print len(a_noisy_list)
    if name_included_in_min_levenshtein_distance(name=a_noisy_list[0],
                                                 target_et=artist_parsed):
        for a_name in a_noisy_list:
            if len(a_name) > 3:
                final_artist.add(a_name)
    if name_included_in_min_levenshtein_distance(name=a_noisy_list[0],
                                                 target_et=songs_parsed):
        for a_name in a_noisy_list:
            final_song.add(a_name)

persist_set(target_set=final_artist,
            file_path="files/final_noisy_artists.txt")

persist_set(target_set=final_song,
            file_path="files/final_noisy_songs.txt")

print "Final noisy artists:", len(final_artist)
print "Final noisy songs:", len(final_song)

# print artist_parsed
# print "----"
# print songs_parsed
# print "----"
# print final_song
# print "-----"
# print final_artist
# print len(final_artist)
