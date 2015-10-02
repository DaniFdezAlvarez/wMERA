__author__ = 'Dani'


def read_manually_discarded_keys(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        for line in file_io:
            if line.endswith("\n"):
                line = line[0:-1]
            if line != "":
                result.add(line)
    return result


def get_tabbed_elements_of_file(file_path, discarded):
    with open(file_path, "r") as file_io:
        line = file_io.readline()
        elements = line.split("\t")
        for elem in elements:
            if elem != "" and elem not in discarded:
                yield elem


def read_song_and_artist_keys(discarded, paths):
    result = set()
    for a_path in paths:
        for elem in get_tabbed_elements_of_file(a_path, discarded):
            result.add(elem.lower())
    return result


def count_keys(keyset, target_str):
    counter = 0
    for a_key in keyset:
        if a_key in target_str:
            target_str = target_str.replace(a_key, "", 1)
            counter += 1
    return counter