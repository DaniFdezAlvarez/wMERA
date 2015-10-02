__author__ = 'Dani'

from test.useful_code.tsv_adapter.parsers.discogs_artist_parser import DiscogsArtistParser
from test.useful_code.tsv_adapter.adapters.artist_tsv_adapter import artist_to_tsv


def read_artists():
    artist_parser = DiscogsArtistParser("discogs_artists.xml")
    for artist in artist_parser.parse_artist():
        yield artist_to_tsv(artist)


# def to_decoded_string(original):
#     result = original.encode(encoding="latin_1")
#     return result.decode(encoding='latin-1').encode(encoding='utf-8')

with open('result_file.tsv', 'w') as result_file:
    errorcount = 0
    artistcount = 0
    exceptioncount = 0
    for artist in read_artists():
        artistcount += 1
        try:
            if "" == artist:
                errorcount += 1
            else:
                # print to_decoded_string(artist + "\n")
                result_file.write(artist + "\n")
        except:
            print artist + "\n"
            errorcount += 1
    print artistcount
    print errorcount
    print exceptioncount


