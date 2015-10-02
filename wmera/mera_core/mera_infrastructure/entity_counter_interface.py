__author__ = 'Dani'


ARTIST_TYPE = "artists"
SONG_TYPE = "songs"


class EntityCounterInterface(object):

    def reset_count(self, types=None):
        """
        If types is None, it will reset all the counts.
        Else, it expects types to be a list of string containing types
        of entity counts to reset.

        :param types:
        :return:
        """
        raise NotImplementedError()

    def increase_artists(self, num_artists=1):
        """
        Increse in num_artists units the stored number of artist present in the graph.
        :param num_artists:
        :return:
        """
        raise NotImplementedError()


    def number_of_artists(self):
        """
        It returns the total number of artist stored in the system.
        :return:
        """
        raise NotImplementedError()


    def increase_songs(self, num_songs=1):
        """
        Increase in num_songs units the stored number of songs present in the graph.

        :param num_songs:
        :return:
        """
        raise NotImplementedError()


    def number_of_songs(self):
        """
        It returns the total number of songs stored in the system.

        :return:
        """
        raise NotImplementedError()




