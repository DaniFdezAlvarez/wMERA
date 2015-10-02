__author__ = 'Dani'


class ArtistParserInterface(object):
    """
    Abstract class that every Artist parsed should implement
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


    def parse_artists(self):
        """
        It should YIELD as many Artist model objects as present in whatever we are parsing.
        :return: generator yielding artist model objects
        """
        raise NotImplementedError("You are calling the method of the interface")

