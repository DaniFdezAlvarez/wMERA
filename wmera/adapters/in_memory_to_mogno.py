__author__ = 'Dani'

from wmera.infrastrusture.in_memory.memory_entity_ngrams import NGRAM


def dump_in_memory_counter_into_mongo_counter(in_memory_repo, mongo_repo):
    n_artist = in_memory_repo.number_of_artists()
    n_songs = in_memory_repo.number_of_songs()
    mongo_repo.reset_count()
    mongo_repo.increase_artists(n_artist)
    mongo_repo.increase_songs(n_songs)


def dump_in_memory_ngrams_into_mongo_ngrams(in_memory_repo, mongo_repo):
    mongo_repo.reset_collection()
    for ngram_key in in_memory_repo._ngrams_dict:  # It should be safe.
        target_dict = in_memory_repo._ngrams_dict[ngram_key]
        target_dict[NGRAM] = ngram_key
        mongo_repo._insert_ngram_dict(target_dict)  # It should be safe.





