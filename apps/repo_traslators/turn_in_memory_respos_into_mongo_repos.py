from wmera.utils import rel_path_to_file

__author__ = 'Dani'

from test.t_utils.t_factory import get_clean_repo_counter_memory, get_clean_repo_song_memory, \
    get_clean_repo_artist_memory, get_clean_repo_artist_mongo, get_clean_repo_counter_mongo, \
    get_clean_repo_songs_mongo

from wmera.adapters.in_memory_to_mogno import dump_in_memory_ngrams_into_mongo_ngrams, \
    dump_in_memory_counter_into_mongo_counter


# Artist ngrmas
mongo_artist = get_clean_repo_artist_mongo()
memory_artist = get_clean_repo_artist_memory()
memory_artist.load_content(rel_path_to_file("../../files/out/artist_ngrams_usos.json",
                                            __file__))

dump_in_memory_ngrams_into_mongo_ngrams(in_memory_repo=memory_artist,
                                        mongo_repo=mongo_artist)
memory_artist = None  # Free memory

# Song ngrams
mongo_song = get_clean_repo_songs_mongo()
memory_song = get_clean_repo_song_memory()
memory_song.load_content(rel_path_to_file("../../files/out/song_ngrams_usos.json",
                                          __file__))

dump_in_memory_ngrams_into_mongo_ngrams(in_memory_repo=memory_song,
                                        mongo_repo=mongo_song)
memory_song = None  # Free memory


# Counter
mongo_counter = get_clean_repo_counter_mongo()
memory_counter = get_clean_repo_counter_memory()
memory_counter.load_content(rel_path_to_file("../../files/out/counter_usos.json",
                                             __file__))

dump_in_memory_counter_into_mongo_counter(in_memory_repo=memory_counter,
                                          mongo_repo=mongo_counter)

