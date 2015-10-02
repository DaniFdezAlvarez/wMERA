__author__ = 'Dani'


class SongParserInterface(object):
    """
    Abstract class that every SongParser should implement
    """

    def __init__(self, dataset):
        """
        It receives a dataset model object with information about the origin of parsed data

        :param dataset:
        :return:
        """

        self._dataset = dataset

    @property
    def dataset(self):
        return self._dataset

    def parse_songs(self):
        """
        It sould YIELD as many Song model objects as present in whatever we are parsing.

        :return: generator yielding discogs model objects
        """
        raise NotImplementedError("You are calling the method of the interface")