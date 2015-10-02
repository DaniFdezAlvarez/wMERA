__author__ = 'Dani'


def read_aol_indexes(file_path):
    result = set()
    with open(file_path, "r") as file_io:
        for line in file_io:
            line = line.replace("\n", "")
            if line != "":
                result.add(int(line))
    return result


def read_musicbrainz_indexes(file_path):
    result = set()
    first_line = True
    with open(file_path, "r") as file_io:
        for line in file_io:
            if first_line:
                first_line = False
            else:
                line = line.replace("\n", "")
                if line != "":
                    result.add(int(line.split("\t")[0]))
    return result



musicbrainz_set = read_musicbrainz_indexes("files/random_musicbrainz.tsv")
aol_set = read_aol_indexes("files/aol_discogs_indexes.txt")
print len(musicbrainz_set)
print len(aol_set)
definitive_set = musicbrainz_set.union(aol_set)
print len(definitive_set)
with open("files/all_discogs_indexes.txt", "w") as file_io:
    for an_index in definitive_set:
        file_io.write(str(an_index) + "\n")
