__author__ = 'Dani'

from wmera.infrastrusture.mongo.mongo_generic_repository import MongoGenericRepository

_TYPE = "type"
_COUNT = "count"


from wmera.mera_core.mera_infrastructure.entity_counter_interface import EntityCounterInterface, ARTIST_TYPE, SONG_TYPE


class EntityCounterRepositoryMongo(MongoGenericRepository, EntityCounterInterface):

    def __init__(self, url_root, collection, host=None, port=None):
        super(EntityCounterRepositoryMongo, self).__init__(url_root, collection, host, port)

    def reset_count(self, types=None):
        """
        If types is None, it will reset all the counts.
        Else, it expects types to be a list of string containing types
        of entity counts to reset.

        :param types:
        :return:
        """
        if types is None:
            types = [ARTIST_TYPE, SONG_TYPE]
        for a_type in types:
            self._db[self._collection].update({_TYPE: a_type},
                                              {"$set": {_COUNT: 0}})


    def increase_artists(self, num_artists=1):
        """
        Increse in num_artists units the stored number of artist present in the graph.
        :param num_artists:
        :return:
        """
        self._increase_entity(num_units=num_artists,
                              type_of_entity=ARTIST_TYPE)

    def number_of_artists(self):
        """
        It returns the total number of artist stored in the system.
        :return:
        """
        return self._number_of_entities(type_of_entity=ARTIST_TYPE)

    def increase_songs(self, num_songs=1):
        """
        Increase in num_songs units the stored number of songs present in the graph.

        :param num_songs:
        :return:
        """
        return self._increase_entity(type_of_entity=SONG_TYPE,
                                     num_units=num_songs)


    def number_of_songs(self):
        """
        It returns the total number of songs stored in the system.

        :return:
        """
        return self._number_of_entities(type_of_entity=SONG_TYPE)


    def _increase_entity(self, num_units, type_of_entity):
        """
        Increase in num_units the count of the entity specified in "type_of_entity"

        :param num_units:
        :param type_of_entity:
        :return:
        """

        self._db[self._collection].update({_TYPE: type_of_entity},
                                          {"$inc": {_COUNT: num_units}})

    def _number_of_entities(self, type_of_entity):
        """
        It returns the total number of entities of type "type_of_entities" stored in the system.

        :param type_of_entity:
        :return:
        """
        doc = self._db[self.collection].find_one({_TYPE: type_of_entity})
        if doc is not None:
            return doc[_COUNT]
        return 0



