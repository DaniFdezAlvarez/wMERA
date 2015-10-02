"""
The repository manages json object with the next base structure:

 {
            NGRAM : ngram
            NUM_APARITIONS : integer with the total number of entities in which the ngram appears,
            ENTITIES : {
                            UriOfAnEntity : integer with the apparitions in that entity,
                            UriOfAnotherEntity : integer,
                            ...
 }

"""

__author__ = 'Dani'
from wmera.infrastrusture.mongo.mongo_generic_repository import MongoGenericRepository
from wmera.mera_core.mera_infrastructure.entity_ngrams_interface import EntityNgramsInterface, ARTIST_COLLECTION, \
    SONG_COLLECTION, ENTITIES, NUM_APPARITIONS, NGRAM





class MongoEntityNgramsRepository(MongoGenericRepository, EntityNgramsInterface):
    def __init__(self, url_root, base_entity_uri, type_of_entity_collection, host=None, port=None):
        if type_of_entity_collection not in [ARTIST_COLLECTION, SONG_COLLECTION]:
            raise ValueError("Invalid type of entity specified to build repo instance")
        super(MongoEntityNgramsRepository, self).__init__(url_root, type_of_entity_collection, host, port)
        self._base_entity_uri = base_entity_uri
        # TODO decide collection from type of entity specified

    def reset_collection(self):
        """
        Remove all the documents of the collection

        :return:
        """
        self._db[self._collection].drop()
        self._db.create_collection(self._collection)
        self._db[self._collection].create_index("ngram", unique=True)



    def update_ngrams_of_entity(self, entity, list_of_tuples_ngram_apparitions):
        """
        It receives the URI of an entity and a list of tuples of two positions.
        That tuples are expected to have an ngram in the first pos and the number
        of new apparitions for the entity specified in the second one. Example:

        entity = "http://example.org/Shakira
        list_of_tuples_ngram_apparitions = [ (sha,9), (kir, 9), (meb, 2),...]

        It checks if the test_ngrams referred have entry in the ddbb, and if not it creates it.
        The same with the entity inside the ngram's list of entities.

        :param entity:
        :param list_of_tuples_ngram_apparitions:
        :return:
        """
        for a_tuple in list_of_tuples_ngram_apparitions:
            self.update_ngram(ngram=a_tuple[0],
                              entity=entity,
                              apparitions=a_tuple[1])

    def update_ngram(self, ngram, entity, apparitions=1):
        """
        It increases in "apparitions" units the apparitions for the entity "entity"
        for the ngram "ngram". If the ngram (or the entity referred) does not have an entry
        to increase, the method creates and initializes it.
        :param ngram:
        :param entity:
        :param apparitions:
        :return:
        """
        # Looking for existing ngram dict or creating it
        is_new_ngram_dict = False
        ngram_dict = self._get_ngram_info_with_ids(ngram)
        if ngram_dict is None:
            is_new_ngram_dict = True
            ngram_dict = MongoEntityNgramsRepository._create_empty_ngram_dict(ngram)

        # Id of the artist in mongo
        entity_name = self._uri_to_id(entity)


        # Increasing entity apparitions in ngram's entity entry
        if entity_name in ngram_dict[ENTITIES]:
            ngram_dict[ENTITIES][entity_name] += apparitions
        else:
            ngram_dict[ENTITIES][entity_name] = apparitions
            ngram_dict[NUM_APPARITIONS] += 1  # Increasing total number of docs in which the ngram appear


        # Updating or inserting dict
        if is_new_ngram_dict:  # This means we have just created the dict
            self._insert_ngram_dict(ngram_dict)
        else:  # It means the dict already existed before executing this
            self._update_ngram_dict(ngram_dict, entity_name)


    def _insert_ngram_dict(self, ngram_dict):
        """
        It inserts ngram_dict in the collection.

        :param ngram_dict:
        :return:
        """
        self._db[self._collection].insert(ngram_dict)


    def _update_ngram_dict(self, ngram_dict, entity_updated=None):
        """
        It looks for the dict in the collection with NGRAM : ngram_dict[NGRAM] and

        - if entity_updated is None :
            it substitutes its fields NUM_APPARITIONS and ENTITIES by the ones of
            ngram_dict
        else:
            it substitutes NUM_APPARITIONS by ngram_dict[NUM_APPARITIONS] and
            ENTITIES[entity_updated] by ngram_dict[ENTITIES][entity_updated]

        :param ngram_dict:
        :return:
        """
        if entity_updated is None:
            self._db[self._collection].update({NGRAM: ngram_dict[NGRAM]},
                                              {"$set": {NUM_APPARITIONS: ngram_dict[NUM_APPARITIONS],
                                                        ENTITIES: ngram_dict[ENTITIES]}})
        else:
            self._db[self._collection].update({NGRAM: ngram_dict[NGRAM]},
                                              {"$set": {NUM_APPARITIONS: ngram_dict[NUM_APPARITIONS],
                                                        ENTITIES + "." + entity_updated:
                                                            ngram_dict[ENTITIES][entity_updated]}})


    def _get_ngram_info_with_ids(self, ngram):
        """
        If the ngram is not in the database, it returns None. If it is, it returns a dict with
        the next structure:

        {
            NGRAM : ngram
            NUM_APARITIONS : integer with the total number of entities in which the ngram appears,
            ENTITIES : {
                            IdOfAnEntity : integer with the apparitions in that entity,
                            IdOfAnotherEntity : integer,
                            ...
                        }

        :param ngram:
        :return:
        """
        ngram_doc = self._db[self.collection].find_one({NGRAM: ngram})
        # If the result of the query was None, None is returned
        return ngram_doc


    def get_ngram_info(self, ngram):
        ngram_doc = self._db[self.collection].find_one({NGRAM: ngram})
        # If the result of the query was None, None is returned
        return self._ngram_info_ids_to_uris(ngram_doc)



    def get_ngram_num_of_apparitions(self, ngram):
        """
        If the ngram is not in the database, it retunrs 0. If it is, it retunrs the number
        of apparitions of the ngram

        :param ngram:
        :return:
        """
        ngram_info = self._get_ngram_info_with_ids(ngram)
        if ngram_info is None:
            return 0
        return ngram_info[NUM_APPARITIONS]


    def get_ngram_entities(self, ngram):
        """
        If the ngram is not in the database, it returns an empty list. If it is, it returns
        a list with the URIs of the entites that contains the ngram in some of their
        name variations.
        :param ngram:
        :return:
        """
        ngram_info = self._get_ngram_info_with_ids(ngram)
        if ngram_info is None:
            return []
        result = []
        for entity_name in ngram_info[ENTITIES]:
            result.append(self._id_to_uri(entity_name))
        return result


    def get_ngram_entities_and_apparitions(self, ngram):
        """
        If the ngram is not in the database, it returns an empty list. If it is, it returns
        a list of tuples with the form (UriOfAnEntity , integer with the apparitions in that entity)

        :param ngram:
        :return:
        """
        ngram_info = self._get_ngram_info_with_ids(ngram)
        if ngram_info is None:
            return []
        result = []
        for entity_name in ngram_info[ENTITIES]:
            result.append((self._id_to_uri(entity_name), ngram_info[ENTITIES][entity_name]))
        return result


    def _id_to_uri(self, original_id):
        return self._base_entity_uri + original_id

    def _uri_to_id(self, uri):
        # WARNING: it is expecting that the received uri ALWAYS starts with self._base_artist_URI
        return uri[len(self._base_entity_uri):]

    def _ngram_info_ids_to_uris(self, ngram_info):
        if ngram_info is None:
            return None
        result = MongoEntityNgramsRepository._create_empty_ngram_dict(ngram_info[NGRAM])
        result[NUM_APPARITIONS] = ngram_info[NUM_APPARITIONS]
        for an_id in ngram_info[ENTITIES]:
            result[ENTITIES][self._id_to_uri(an_id)] = ngram_info[ENTITIES][an_id]
        return result


    @staticmethod
    def _create_empty_ngram_dict(ngram):
        """
        It returns a dict with the structure of a doc to be inserted in mongodb, but empty
        despite of the NGRAM field. This would be the result:

        {
            NGRAM : ngram,
            NUM_APPARITIONS : 0,
            ENTITIES : {
                        }
        }

        :param ngram:
        :return:
        """
        return {NGRAM: ngram,
                NUM_APPARITIONS: 0,
                ENTITIES: {}}








