__author__ = 'Dani'

import random
from aol_utils import read_song_and_artist_keys, read_manually_discarded_keys, count_keys


manually_discarded_keys = read_manually_discarded_keys("files/discarded_keys.txt")
keyset = read_song_and_artist_keys(manually_discarded_keys,
                                    ["files/final_noisy_songs.txt",
                                     "files/final_noisy_artists.txt"])
arr1 = []
arr2_3 = []
arr4_plus = []

with open("files/relevant_randomized_queries.txt", "r") as rel_q_io:
    counter = 0
    for a_line in rel_q_io:
        counter += 1
        if counter % 100 == 0:
            print "I have done", counter
        n_keys = count_keys(keyset, a_line[0:-1])  # Removing "\n" char
        query_str = str(n_keys) + "\t" + a_line
        if n_keys == 1:
            arr1.append(query_str)
        elif n_keys >= 4:
            arr4_plus.append(query_str)
        else:
            arr2_3.append(query_str)

random.shuffle(arr1)
random.shuffle(arr2_3)
random.shuffle(arr4_plus)

with open("files/out/relevant_key_clasified.txt", "w") as result_io:
    for elem in arr1:
        result_io.write(elem)
    for elem in arr2_3:
        result_io.write(elem)
    for elem in arr4_plus:
        result_io.write(elem)
