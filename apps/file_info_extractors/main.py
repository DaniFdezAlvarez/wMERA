__author__ = 'Dani'

from apps.file_info_extractors.bmat_extractor import BmatExtractor
from apps.file_info_extractors.cwr_extractor import CwrExtarctor

path = "../files/bmat2heaven.tsv"
url = '156.35.82.103:9090'

bmat_extractor = BmatExtractor(path)
cwr_extractor = CwrExtarctor(url)

bmats = bmat_extractor.get_random_artist_names(150)
cwrs = cwr_extractor.get_ramdom_writers_names(150)

counter = 0
for artist in bmats:
    counter += 1
    print artist, counter
print "-----------------------------------------"
counter = 0
for artist in cwrs:
    counter += 1
    print artist, counter

with open("random_real_names.txt", "w") as result_file:
    result_file.write("\t".join(bmats) + "\n")
    result_file.write("\t".join(cwrs) + "\n")

