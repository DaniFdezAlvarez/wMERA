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

import json

__author__ = 'Dani'

from wmera.mera_core.mera_infrastructure.entity_ngrams_interface import EntityNgramsInterface, NGRAM, NUM_APPARITIONS, \
    ENTITIES, ARTIST_COLLECTION, SONG_COLLECTION


class MemoryEntityNgrams(EntityNgramsInterface):

    def __init__(self, base_entity_uri, type_of_entity_collection, load_file=None):
        if type_of_entity_collection not in [ARTIST_COLLECTION, SONG_COLLECTION]:
            raise ValueError("Invalid type of entity specified to build repo instance")
        self._ngrams_dict = {}
        if load_file is not None:
            self.load_content(load_file)
        self._base_entity_uri = base_entity_uri
        self._type_of_entity_collection = type_of_entity_collection


    ##### Implementation of EntityNgramsInterface

    def reset_collection(self):
        """
        Remove all the documents of the collection

        :return:
        """
        self._ngrams_dict = {}


    def get_ngram_info(self, ngram):
        """
        If the result of the query is None, None is returned.
        Else, return the dict associated with the ngram

        :param ngram:
        :return:
        """
        if ngram not in self._ngrams_dict:
            return None
        else:
            return self._internal_dict_to_external_dict(ngram, self._ngrams_dict[ngram])


    def get_ngram_num_of_apparitions(self, ngram):
        """
        If the ngram is not in the database, it retunrs 0. If it is, it retunrs the number
        of apparitions of the ngram

        :param ngram:
        :return:
        """
        if ngram not in self._ngrams_dict:
            return 0
        else:
            return self._ngrams_dict[ngram][NUM_APPARITIONS]


    def get_ngram_entities(self, ngram):
        """
        If the ngram is not in the database, it returns an empty list. If it is, it returns
        a list with the URIs of the entities that contains the ngram in some of their
        name variations.
        :param ngram:
        :return:
        """
        if ngram not in self._ngrams_dict:
            return []
        result = []
        for an_id in self._ngrams_dict[ngram][ENTITIES]:
            result.append(self._id_to_uri(an_id))
        return result


    def get_ngram_entities_and_apparitions(self, ngram):
        """
        If the ngram is not in the database, it returns an empty list. If it is, it returns
        a list of tuples with the form (UriOfAnEntity , integer with the apparitions in that entity)

        :param ngram:
        :return:
        """
        if ngram not in self._ngrams_dict:
            return []
        result = []
        for an_id in self._ngrams_dict[ngram][ENTITIES]:
            result.append((self._id_to_uri(an_id), self._ngrams_dict[ngram][ENTITIES][an_id]))
        return result


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
        entity_id = self._uri_to_id(entity)
        for a_tuple in list_of_tuples_ngram_apparitions:
            self._update_ngram_through_id(ngram=a_tuple[0],
                                          entity_id=entity_id,
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
        self._update_ngram_through_id(ngram=ngram,
                                      entity_id=self._uri_to_id(entity),
                                      apparitions=apparitions)

#######  Special public methods


    def save_content(self, file_path):
        with open(file_path, "w") as file_content:
            json.dump(self._ngrams_dict, file_content)


    def load_content(self, file_path):
        with open(file_path, "r") as file_content:
            self._ngrams_dict = json.load(file_content)



#######   Private methods

    def _get_ngram_info_with_ids(self, ngram):
        if ngram not in self._ngrams_dict:
            return None
        result = self._internal_dict_to_external_dict(ngram, self._ngrams_dict[ngram])
        tmp_entities = result[ENTITIES]
        result[ENTITIES] = {}
        for an_uri in tmp_entities:
            result[ENTITIES][self._uri_to_id(an_uri)] = tmp_entities[an_uri]
        return result


    def _internal_dict_to_external_dict(self, ngram, internal_dict):
        result = {NUM_APPARITIONS: internal_dict[NUM_APPARITIONS],
                  NGRAM: ngram,
                  ENTITIES: {}}
        for an_entity in internal_dict[ENTITIES]:
            result[ENTITIES][self._id_to_uri(an_entity)] = internal_dict[ENTITIES][an_entity]
        return result


    def _id_to_uri(self, original_id):
        return self._base_entity_uri + original_id


    def _uri_to_id(self, uri):
        # WARNING: it is expecting that the received uri ALWAYS starts with self._base_artist_URI
        return uri[len(self._base_entity_uri):]


    def _update_ngram_through_id(self, ngram, entity_id, apparitions):
        if ngram not in self._ngrams_dict:
            self._ngrams_dict[ngram] = self._create_empty_internal_dict()
        if entity_id not in self._ngrams_dict[ngram][ENTITIES]:
            self._ngrams_dict[ngram][ENTITIES][entity_id] = 0
            self._ngrams_dict[ngram][NUM_APPARITIONS] += 1
        self._ngrams_dict[ngram][ENTITIES][entity_id] += apparitions


    @staticmethod
    def _create_empty_internal_dict():
        return {NUM_APPARITIONS: 0,
                ENTITIES: {}}


