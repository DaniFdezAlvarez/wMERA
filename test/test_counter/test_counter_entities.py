__author__ = 'Dani'

import unittest

from test.t_utils.t_factory import get_clean_repo_counter_mongo, get_clean_repo_counter_memory


class TestCounterEntities(unittest.TestCase):


    def test_counter_mongo(self):
        self._batery_with_a_concrete_repo(get_clean_repo_counter_mongo())


    def test_counter_memory(self):
        self._batery_with_a_concrete_repo(get_clean_repo_counter_memory())


    def _batery_with_a_concrete_repo(self, repo_counter):

        # No entities
        self.assertEquals(0, repo_counter.number_of_artists())
        self.assertEquals(0, repo_counter.number_of_songs())

        # Adding a song
        repo_counter.increase_songs()
        self.assertEquals(0, repo_counter.number_of_artists())
        self.assertEquals(1, repo_counter.number_of_songs())

        # Adding several songs
        repo_counter.increase_songs(3)
        self.assertEquals(0, repo_counter.number_of_artists())
        self.assertEquals(4, repo_counter.number_of_songs())

        # Adding an artist
        repo_counter.increase_artists()
        self.assertEquals(1, repo_counter.number_of_artists())
        self.assertEquals(4, repo_counter.number_of_songs())

        # Adding several artists
        repo_counter.increase_artists(5)
        self.assertEquals(6, repo_counter.number_of_artists())
        self.assertEquals(4, repo_counter.number_of_songs())

        # Reset
        repo_counter.reset_count()
        self.assertEquals(0, repo_counter.number_of_artists())
        self.assertEquals(0, repo_counter.number_of_songs())

        # Working after reset
        repo_counter.increase_artists(5)
        repo_counter.increase_songs()
        self.assertEquals(5, repo_counter.number_of_artists())
        self.assertEquals(1, repo_counter.number_of_songs())

