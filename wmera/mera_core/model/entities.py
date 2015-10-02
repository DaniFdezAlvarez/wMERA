__author__ = 'Dani'


# ########## MUSICAL ENTITIES #################################

TYPE_SET = 'type_set'


class MusicalEntity(object):
    """
    Abstract. Every musical entity should inherit from this in order to have a canonical name
    """

    def __init__(self, canonical):
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if MusicalEntity not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(MusicalEntity)
            # print "MusicalEntity", canonical
            self._canonical = canonical

    @property
    def canonical(self):
        return self._canonical


class Song(MusicalEntity):

    def __init__(self, canonical, artists=None, collaborations=None, duration=None,
                 genres=None, release_date=None, album=None,
                 alt_titles=None, country=None, discogs_id=None, discogs_index=None,
                 usos_transaction_id=None, usos_isrc=None, iswc=None):
        """

        :param canonical: str
        :param artists: list of artist obj
        :param collaborations: list of collaboration objects
        :param duration: int (seconds)
        :param genres: list of strings
        :param release_date: not sure really # TODO
        :param album: album object
        :param alt_titles: list of strings
        :param country: string
        :return:
        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if Song not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(Song)
            #TODO decide date type
            super(Song, self).__init__(canonical)

            if artists is None:
                artists = []
            self._artists = artists
            if collaborations is None:
                collaborations = []
            self._collaborations = collaborations
            self._duration = duration
            if genres is None:
                genres = []
            self._genres = genres
            self._release_date = release_date
            self._album = album
            if alt_titles is None:
                alt_titles = []
            self._alt_titles = alt_titles
            self._country = country
            self._discogs_id = discogs_id
            self._discogs_index = discogs_index
            self._usos_transaction_id = usos_transaction_id
            self._usos_isrc = usos_isrc
            self._iswc = iswc


    @property
    def iswc(self):
        return self._iswc

    @property
    def usos_transaction_id(self):
        return self._usos_transaction_id


    @property
    def usos_isrc(self):
        return self._usos_isrc


    @property
    def discogs_id(self):
        return self._discogs_id


    @property
    def discogs_index(self):
        return self._discogs_index


    @property
    def artists(self):
        for artist in self._artists:
            yield artist


    def add_artist(self, artist):
        self._artists.append(artist)


    @property
    def collaborations(self):
        for collaboration in self._collaborations:
            yield collaboration


    def add_collaboration(self, collaboration):
        """

        :param collaboration: Collaboration object
        :return:
        """
        self._collaborations.append(collaboration)

    @property
    def genres(self):
        for genre in self._genres:
            yield genre


    def add_genre(self, genre):
        self._genres.append(genre)


    @property
    def release_date(self):
        return self._release_date


    @property
    def alternative_titles(self):
        for title in self._alt_titles:
            yield title


    def add_alternative_title(self, title):
        self._alt_titles.append(title)


    @property
    def country(self):
        return self._country


    @property
    def album(self):
        return self._album






class Artist(MusicalEntity):
    def __init__(self, canonical, aliases=None, namevars=None, country=None, discogs_id=None):
        """
            :param canonical: str
            :param aliases: list of str
            :param namevars: list of str
            :param country: str
            :return:
        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if Artist not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(Artist)
            # print "Artist", canonical
            super(Artist, self).__init__(canonical)

            if namevars is None:
                namevars = []
            self._namevars = namevars

            if aliases is None:
                aliases = []
            self._aliases = aliases

            self._country = country
            self._discogs_id = discogs_id



    @property
    def discogs_id(self):
        return self._discogs_id

    @property
    def namevars(self):
        """
        generator
        :return:
        """
        for avar in self._namevars:
            yield avar

    @property
    def country(self):
        return self._country


    def add_namevar(self, namevar):
        self._namevars.append(namevar)


    @property
    def aliases(self):
        """
        generator
        :return:
        """
        for alias in self._aliases:
            yield alias


    def add_alias(self, alias):
        self._aliases.append(alias)


class ArtistPerson(Artist):
    def __init__(self, canonical, civil=None, aliases=None, namevars=None, country=None, discogs_id=None):
        """

        :param canonical:
        :param civil:
        :param namevars:
        :param country:
        :param aliases: list of str
        :return:
        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if ArtistPerson not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(ArtistPerson)
            # print "ArtistPerson", canonical
            super(ArtistPerson, self).__init__(canonical, aliases, namevars, country, discogs_id)
            self._civil = civil


    @property
    def civil(self):
        return self._civil


class ArtistGroup(Artist):
    def __init__(self, canonical, aliases=None, namevars=None, country=None, members=None, discogs_id=None):
        """
        :param members: list of ArtistPerson objects

        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if ArtistGroup not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(ArtistGroup)
            super(ArtistGroup, self).__init__(canonical, aliases, namevars, country, discogs_id)
            if members is None:
                members = []
            self._members = members


    @property
    def members(self):
        return self._members


    def add_member(self, artist_person):
        """
        It expects to receive an artist_person object

        """
        self._members.append(artist_person)


########### OTHER ENTITIES ######################

ROLE_WRITER = "Writer"
ROLE_FEATURER = "Featurer"




class Collaboration(object):
    """
    Used for link an artist/person with a role played in a determinated work
    """

    def __init__(self, collaborator, role):
        """
        :param collaborator: an Artist instance
        :param role: a string from a known range

        """
        # The range of roles are the string specified in this file
        # named with the regexp ROLE_.+
        # Im not planing to to a code checking (we are pythonic adults),
        # but it would be safer.

        self._collaborator = collaborator
        self._role = role

    @property
    def collaborator(self):
        return self._collaborator

    @property
    def role(self):
        return self._role

    @staticmethod
    def valid_roles():
        """
        It return a list containing all the recognized roles for collaborations
        """
        return [ROLE_WRITER, ROLE_FEATURER]


class Dataset(object):
    """
    Represents a set of information
    """

    def __init__(self, title, description=None, download_link=None, home_page=None, date=None):
        """
        :param title: str with a name for the dataset
        :param download_link: link to dowload the data
        :param home_page: possible homepage of the org who provides the data
        :param date: STRING. It will not be used for comparisons. Just to build an identificative URI.
                    As precise as it could be. Desired format: dd-mm-yyyy. No need to provide all the fields,
                    but need to use "-" as separator in case to provide several.
        :param description: str describing the content of the dataset

        """
        self._title = title
        self._download_link = download_link
        self._home_page = home_page
        self._date = date
        self._description = description

    @property
    def title(self):
        return self._title

    @property
    def download_link(self):
        return self._download_link

    @property
    def home_page(self):
        return self._home_page

    @property
    def date(self):
        return self._date

    @property
    def description(self):
        return self._description



