__author__ = 'Dani'
import random

from aol_utils import read_manually_discarded_keys, read_song_and_artist_keys










def read_relevant_queries(file_path):
    result = []
    with open(file_path, "r") as file_io:
        for line in file_io:
            line = line[0: -1]  # Erasing final "\n" char
            line = line.split("\t")[1]  # Selecting query consult
            result.append(line.lower())
    return result



def qet_query_pieces(original_query):
    candidate_pieces = original_query.replace("\n", "").lower().split(" ")
    result = []
    for a_c_piece in candidate_pieces:
        if a_c_piece != "":
            result.append(a_c_piece)
    return result


def get_query_pieces_combinations(query_pieces):
    result = []
    i = 0
    j = 1
    while i < len(query_pieces):
        j = i + 1
        while j <= len(query_pieces):
            result.append(" ".join(query_pieces[i:j]))
            j += 1
        i += 1
    return result



def is_relevant_query(query, keyset):
    query_pieces = query.replace("\n", "").split(" ")
    query_substrings = get_query_pieces_combinations(query_pieces)
    for a_subs in query_substrings:
        if a_subs in keyset:
            return True
    return False



######################## ----------- PROGRAM ----------- ####################################


relevant_queries_path = "files/relevant_queries.txt"
randomized_queries_path = "files/relevant_randomized_queries.txt"
manually_discarded_keys = read_manually_discarded_keys("files/discarded_keys.txt")
target_keys = read_song_and_artist_keys(manually_discarded_keys,
                                        ["files/final_noisy_songs.txt",
                                         "files/final_noisy_artists.txt"])


# for key in target_keys:
#     print key

# print is_relevant_query("une shakira Mebarach", target_keys)

counter = 0
with open("../../files/consultas_aol/consultas-AOL.txt", "r") as queries_aol_io:
    with open(relevant_queries_path, "w") as relevant_queries_io:
        for line in queries_aol_io:
            counter += 1
            if counter % 100000 == 0:
                print "I've done ", counter

            if is_relevant_query(line, target_keys):
                relevant_queries_io.write(line)

relevant_queries = read_relevant_queries("files/relevant_queries.txt")
random.shuffle(relevant_queries)
with open(randomized_queries_path, "w") as file_randomized:
    for a_query in relevant_queries:
        file_randomized.write(a_query + "\n")

