__author__ = 'Dani'

import unittest

from wmera.infrastrusture.mongo.ngrams.mongo_entity_ngrams import NUM_APPARITIONS, ENTITIES, NGRAM
from wmera.graph_gen.rdflib.rdf_utils.namespaces_handler import base_entities_URI
from test.t_utils.t_factory import get_clean_repo_artist_mongo, get_clean_repo_artist_memory


## Creating

class TestNgrams(unittest.TestCase):

    def test_ngrams_mongo(self):
        self._battery_with_a_concrete_repo(get_clean_repo_artist_mongo())


    def test_ngrams_in_memory(self):
        self._battery_with_a_concrete_repo(get_clean_repo_artist_memory())



    def _battery_with_a_concrete_repo(self, artists_ngram_repo):
        # Creating

        artists_ngram_repo.update_ngram(ngram="foo", entity=base_entities_URI + "chancleto", apparitions=2)
        foo_info = artists_ngram_repo.get_ngram_info(ngram="foo")

        foo_info_ids = artists_ngram_repo._get_ngram_info_with_ids(ngram="foo")

        self.assertEquals(foo_info[NGRAM], "foo")
        self.assertEquals(foo_info[ENTITIES][base_entities_URI + "chancleto"], 2)
        self.assertEquals(foo_info_ids[ENTITIES]["chancleto"], 2)
        self.assertEquals(foo_info[NUM_APPARITIONS], 1)


        ## Updating

        artists_ngram_repo.update_ngram(ngram="foo", entity=base_entities_URI + "chancleto", apparitions=2)
        foo_info = artists_ngram_repo.get_ngram_info(ngram="foo")
        foo_info_ids = artists_ngram_repo._get_ngram_info_with_ids(ngram="foo")

        self.assertEquals(foo_info[NGRAM], "foo")
        self.assertEquals(foo_info[ENTITIES][base_entities_URI + "chancleto"], 4)
        self.assertEquals(foo_info_ids[ENTITIES]["chancleto"], 4)
        self.assertEquals(foo_info[NUM_APPARITIONS], 1)


        ## With a new one

        artists_ngram_repo.update_ngram(ngram="foo", entity=base_entities_URI + "chancleto", apparitions=2)
        foo_info = artists_ngram_repo.get_ngram_info(ngram="foo")
        foo_info_ids = artists_ngram_repo._get_ngram_info_with_ids(ngram="foo")

        artists_ngram_repo.update_ngram(ngram="fee", entity=base_entities_URI + "chancleto", apparitions=3)
        fee_info = artists_ngram_repo.get_ngram_info(ngram="fee")
        fee_info_ids = artists_ngram_repo._get_ngram_info_with_ids(ngram="fee")

           # About foo
        self.assertEquals(foo_info[NGRAM], "foo")
        self.assertEquals(foo_info[ENTITIES][base_entities_URI + "chancleto"], 6)
        self.assertEquals(foo_info_ids[ENTITIES]["chancleto"], 6)
        self.assertEquals(foo_info[NUM_APPARITIONS], 1)

            # About fee
        self.assertEquals(fee_info[NGRAM], "fee")
        self.assertEquals(fee_info[ENTITIES][base_entities_URI + "chancleto"], 3)
        self.assertEquals(fee_info_ids[ENTITIES]["chancleto"], 3)
        self.assertEquals(fee_info[NUM_APPARITIONS], 1)


        ### No ngrmam

        none_info = artists_ngram_repo.get_ngram_info(ngram="Non")
        self.assertIsNone(none_info)

        ### In more documents updating

        artists_ngram_repo.update_ngram(ngram="foo", entity=base_entities_URI + "chancletin", apparitions=1)
        foo_info = artists_ngram_repo.get_ngram_info(ngram="foo")
        foo_info_ids = artists_ngram_repo._get_ngram_info_with_ids(ngram="foo")

        self.assertEquals(foo_info[NGRAM], "foo")
        self.assertEquals(foo_info[ENTITIES][base_entities_URI + "chancleto"], 6)
        self.assertEquals(foo_info_ids[ENTITIES]["chancleto"], 6)
        self.assertEquals(foo_info[ENTITIES][base_entities_URI + "chancletin"], 1)
        self.assertEquals(foo_info_ids[ENTITIES]["chancletin"], 1)
        self.assertEquals(foo_info[NUM_APPARITIONS], 2)

