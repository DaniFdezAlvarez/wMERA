__author__ = 'Dani'

from test.useful_code.tsv_adapter.utils.util_tsv_adapter import list_to_tsv_field


def artist_to_tsv(artist):
    if artist.name is None:
        return ""
    result = artist.name + "\t" + list_to_tsv_field(artist.real_name) + "\t" + artist.data_quality +\
           '\t' + list_to_tsv_field(artist.name_variations) + "\t" + list_to_tsv_field(artist.aliases)
    try:
        result = result.encode("latin_1")
        return result.decode("latin_1").encode("utf-8")
    except:
        return ""



