__author__ = 'Dani'

from wmera.mera_core.str_ops.ngrams import extract_unique_normalized_ngrmas


# _artsit_repo = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
#                                       base_entity_uri=base_entities_URI,
#                                       type_of_entity_collection=ARTIST_COLLECTION)
#
# _song_repo = MongoEntityNgramsRepository(url_root="127.0.0.1:27017",
#                                     base_entity_uri=base_entities_URI,
#                                     type_of_entity_collection=SONG_COLLECTION)


def update_ngrams_of_entity(repo, entity_uri, str_text):
    tuples = []
    for ngram in extract_unique_normalized_ngrmas(str_text):
        tuples.append((ngram, 1))
    repo.update_ngrams_of_entity(entity=entity_uri,
                                 list_of_tuples_ngram_apparitions=tuples)

