__author__ = 'Dani'

"""
This methods should probably be included in a class receiving a ins tance of a repo.
Otherwise, we are unnecessarily linking them to the mongo repo

"""


def increase_artist_count(entity_counter_repo):
    """
    Increases in 1 the artist count in the repo.
    :return:
    """
    entity_counter_repo.increase_artists()


def increase_song_count(entity_counter_repo):
    """
    Increases in 1 the discogs count in the repo.
    :return:
    """
    entity_counter_repo.increase_songs()
