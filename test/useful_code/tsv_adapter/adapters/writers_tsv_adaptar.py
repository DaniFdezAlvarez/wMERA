__author__ = 'Dani'


def artist_to_tsv(artist):
    if artist.name is None:
        return ""
    result = artist.name + "\t" + artist.name + "\t" + artist.data_quality + "\t\t"
    try:
        result = result.encode("latin_1")
        return result.decode("latin_1").encode("utf-8")
    except:
        return ""