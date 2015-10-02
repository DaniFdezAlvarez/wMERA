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


# ## KEYS IN DOCUMENTS
NUM_APPARITIONS = "times"
ENTITIES = "entities"
NGRAM = "ngram"


# ## TYPES OF ENTITIES TO SPECIFY IN __init__

ARTIST_COLLECTION = "artist_ngrams"
SONG_COLLECTION = "song_ngrams"


class EntityNgramsInterface(object):

    def reset_collection(self):
        """
        Remove all the documents of the collection

        :return:
        """
        raise NotImplementedError()


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
        raise NotImplementedError()


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
        raise NotImplementedError()


    def get_ngram_info(self, ngram):
        """
        If the result of the query is None, None is returned.
        Else, return the dict associated with the ngram

        :param ngram:
        :return:
        """
        raise NotImplementedError()


    def get_ngram_num_of_apparitions(self, ngram):
        """
        If the ngram is not in the database, it retunrs 0. If it is, it retunrs the number
        of apparitions of the ngram

        :param ngram:
        :return:
        """
        raise NotImplementedError()


    def get_ngram_entities(self, ngram):
        """
        If the ngram is not in the database, it returns an empty list. If it is, it returns
        a list with the URIs of the entites that contains the ngram in some of their
        name variations.
        :param ngram:
        :return:
        """
        raise NotImplementedError()


    def get_ngram_entities_and_apparitions(self, ngram):
        """
        If the ngram is not in the database, it returns an empty list. If it is, it returns
        a list of tuples with the form (UriOfAnEntity , integer with the apparitions in that entity)

        :param ngram:
        :return:
        """
        raise NotImplementedError()





