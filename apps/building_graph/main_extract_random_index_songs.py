__author__ = 'Dani'

import random

NUM_SONGS = 45458287  # 45.458.287
DESIRED_SONGS = 500000  # 500.000


def read_necessary_index_songs(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        for line in file_io:
            line = line.replace("\n","")
            if line != "":
                result.add(int(line))
    return result


def generate_several_indexes_from_a_known_range(preliminar, min_value, max_value, desired):
    result = set().union(preliminar)
    while len(result) < desired:
        result.add(random.randint(min_value, max_value))
    return result



preliminar_set_of_songs = read_necessary_index_songs("files/all_discogs_indexes.txt")
whole_set_of_songs = generate_several_indexes_from_a_known_range(preliminar=preliminar_set_of_songs,
                                                                 min_value=0,
                                                                 max_value=NUM_SONGS,
                                                                 desired=DESIRED_SONGS)

with open("files/500000_discogs_song_indexes.txt", "w") as file_io:
    for an_index in whole_set_of_songs:
        file_io.write(str(an_index) + "\n")

