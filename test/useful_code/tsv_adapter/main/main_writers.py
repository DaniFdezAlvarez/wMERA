__author__ = 'Dani'

from test.useful_code.tsv_adapter.parsers.discogs_writers_parser import DiscogsWriterParser
from test.useful_code.tsv_adapter.adapters.artist_tsv_adapter import artist_to_tsv


def read_writers():
    artist_parser = DiscogsWriterParser("discogs_releases.xml")
    for artist in artist_parser.parse_artist():
        yield artist_to_tsv(artist)


# def to_decoded_string(original):
#     result = original.encode(encoding="latin_1")
#     return result.decode(encoding='latin-1').encode(encoding='utf-8')

with open('../../files/discog_writers.tsv', 'w') as result_file:
    errorcount = 0
    writerscount = 0
    exceptioncount = 0
    for writer in read_writers():
        writerscount += 1
        if writerscount % 100000 == 0:
            print "Llevamos hechos", writerscount
        try:
            if "" == writer:
                errorcount += 1
            else:
                result_file.write(writer + "\n")
        except:
            print writer + "\n"
            errorcount += 1
    print writerscount
    print errorcount
    print exceptioncount