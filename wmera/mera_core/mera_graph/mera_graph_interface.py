__author__ = 'Dani'


class MeraGraphInterface(object):
    """
    The methods return Mera model objects
    """


    def get_artist_by_uri(self, uri):
        raise NotImplementedError()

    def get_artist_person_by_uri(self, uri):
        raise NotImplementedError()


    def get_artist_group_by_uri(self, uri):
        raise NotImplementedError()


    def get_song_by_uri(self, uri):
        raise NotImplementedError()


    def get_songs_of_artist(self, uri):
        raise NotImplementedError()

    def get_artists_and_collaborators_of_song_by_uri(self, uri):
        raise NotImplementedError()

    def get_uri_of_intermediary_of_text(self, primary_entity_uri, primary_property, matching_text):
        raise NotImplementedError()

    def get_uri_of_intermediary_of_entity(self, primary_entity_uri, primary_property, target_entity_uri):
        raise NotImplementedError()

    def __contains__(self, triple):
        raise NotImplementedError()

    def add_triple(self, triple):
        raise NotImplementedError()

    def already_exist_in_graph(self, uri):
        raise NotImplementedError()

    def serialize(self, out_format='turtle'):
        """
        Lets say that the available outout formats should be the same that rdflib offers.
        :param out_format:
        :return:
        """
        raise NotImplementedError()