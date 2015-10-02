__author__ = 'Dani'

from wmera.mera_core.model.entities import Dataset, ROLE_WRITER
from wmera.parsers.discogs.song_parser import DiscogsSongParser
from wmera.utils import rel_path_to_file

import random


def count_releases(parser):
    counter = 0
    for song in parser.parse_songs():
        counter += 1
        if counter % 100000 == 0:
            print "Llevo " + str(counter)

    print "En total hay", counter, "canciones"
    return counter


def fast_search_with_elimination_if_found(a_list, elem):
    if a_list[0] == elem:
        a_list.pop(0)
        return True
    else:
        return False


def generate_sorted_aleatory_list(num_elems, min_val, max_val):
    set_result = set()
    while len(set_result) != num_elems:
        set_result.add(random.randint(min_val, max_val))
    list_result = list(set_result)
    list_result.sort()
    return list_result


def get_desired_songs(parser, indexes):
    trace_counter = 0
    last_index = indexes[len(indexes) - 1]
    counter = 0
    result = []
    for song in parser.parse_songs():
        trace_counter += 1
        if trace_counter % 100000 == 0:
            print "I have parsed " + str(trace_counter)
        if fast_search_with_elimination_if_found(indexes, counter):
            result.append((counter, song))
        counter += 1
        if counter == last_index:
            break

    return result



def split_in_number_of_artist_lists(songs):
    art1 = []
    art2_3 = []
    art4_plus = []

    for song_tuple in songs:
        a_song = song_tuple[1]
        set_people = set()
        artists_count = 0
        for artist in a_song.artists:
            set_people.add(artist.canonical)
        writers_count = 0
        for coll in a_song.collaborations:
            if coll.role == ROLE_WRITER:
                set_people.add(coll.collaborator.canonical)
        num_artist = len(set_people)
        if num_artist == 0:
            print "Mecachis en la mar...."
            pass  # Song discarded
        elif num_artist == 1:
            art1.append(song_tuple)
        elif num_artist <= 3:
            art2_3.append(song_tuple)
        else:  # 4+ artists
            print num_artist
            art4_plus.append(song_tuple)

    random.shuffle(art1)
    random.shuffle(art2_3)
    random.shuffle(art4_plus)


    return art1, art2_3, art4_plus


def serialize_song_tsv_artist(song_tuple):
    a_song = song_tuple[1]
    result = str(song_tuple[0]) + "\t" + a_song.canonical
    for artist in a_song.artists:
        result += "\t" + artist.canonical
    for coll in a_song.collaborations:
        if coll.role == ROLE_WRITER:
            result += "\t" + coll.collaborator.canonical
    return result

# def binary_search_with_elimination_if_found(a_list, elem):
# pos = bisect_left(a_list, elem, 0, len(a_list))
#     if pos != len(a_list) and a_list[pos] == elem:
#         a_list.pop(pos)
#         return True
#     else:
#         return False




def extract_random_tsv_songs(file_path, total_songs, desired_songs):
    releases_parser = DiscogsSongParser(file_path=file_path,
                                        dataset=Dataset(title="TestDataset"))

    elem_index_list = generate_sorted_aleatory_list(min_val=0, max_val=total_songs, num_elems=desired_songs)
    desired_song_objects = get_desired_songs(parser=releases_parser, indexes=elem_index_list)
    art1, art2_3, art4_plus = split_in_number_of_artist_lists(desired_song_objects)

    print len(art1), len(art2_3), len(art4_plus)

    with open("songs_1_artist.tsv", "w") as target_file:
        for song in art1:
            target_file.write(serialize_song_tsv_artist(song) + "\n")

    with open("songs_2_3_artist.tsv", "w") as target_file:
        for song in art2_3:
            target_file.write(serialize_song_tsv_artist(song) + "\n")

    with open("songs_4_plus_artist.tsv", "w") as target_file:
        for song in art4_plus:
            target_file.write(serialize_song_tsv_artist(song) + "\n")


num_songs = 45458287
# num_songs = 100
# desired_songs = 3500


extract_random_tsv_songs(file_path=rel_path_to_file("../../files/discogs_releases.xml", __file__),
                         total_songs=num_songs,
                         desired_songs=3500)







