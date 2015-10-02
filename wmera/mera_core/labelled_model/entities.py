"""

All the MeraEntities have the same structure of the raw entities of the model
but each one of the fields are duplicated , offering a new property in which
the raw field is associated with the source/sources that provided it. That
property comes in the form of a tuple (list of tuples in case the original
raw data was also a list) of two positions, with the next structure:

po0 : original content of the raw entity (a name, an alias, a place,...)

po1 : list containing the URI of the sources from wich that piece of information
        has been provided. It could be more than one, but necessarily one.

Example: We had an ArtsitPerson of the raw model with this structure

        canonical : "Mike"
        civil : "Miguel Mesa"

If the data was originally provided by a dataset of discogs but we also found
that the civil name for that artist was Mike Mesa in a dataset of musicbrainz,
then the resulting MeraArtistPerson would be:

        canonical : "Mike"
        canonical_tuple : ("Mike", ["http://discogs/dataset4"])

        civil : "Miguel Mesa"
        civil_tuple : ("Miguel Mesa, [
                                        "http://discogs/dataset4",
                                        "http://musicbrainz/dataset5"
                                      ])


None of the properties of the raw model is redefined, but all the methods
add_XXX(thing_to_add) should be. The new methods expects to receive a tuple
with the described form (raw_data, [list_of_sources]).

There is not a new method for adding this labelled info because adding
non-labelled info should not be coherent with the structure of Mera model
objects. So, the old add_XXX are redefined.


"""

__author__ = 'Dani'

from wmera.mera_core.model.entities import *

# ########## MUSICAL ENTITIES #################################


class MeraMusicalEntity(MusicalEntity):
    """
    Abstract. Every musical entity should inherit from this in order to have a canonical name and source
    """

    def __init__(self, labelled_canonical):
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if MeraMusicalEntity not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(MeraMusicalEntity)
            # print "MeraMusicalEntity", labelled_canonical
            super(MeraMusicalEntity, self).__init__(canonical=labelled_canonical[0])
            self._labelled_canonical = labelled_canonical

    @property
    def canonical_source(self):
        return self._labelled_canonical[1]

    @property
    def canonical_tuple(self):
        return self._labelled_canonical

    @property
    def identifying_form_tuples(self):
        """
        It returns a generator with all the identifying strings (labelled)
        of the instance
        :return:
        """
        yield self._labelled_canonical

    @property
    def identifying_forms(self):
        """
        It returns a generator with all the identifying strings (labelled)
        of the instance
        :return:
        """
        yield self._canonical


class MeraSong(Song, MeraMusicalEntity):
    def __init__(self, labelled_canonical, artists=None, labelled_collaborations=None, duration=None,
                 labelled_genres=None, release_date=None, album=None,
                 labelled_alt_titles=None, labelled_country=None, discogs_id=None, discogs_index=None,
                 usos_transaction_id=None, usos_isrc=None, iswc=None):

        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if MeraSong not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(MeraSong)

            if labelled_collaborations is None:
                labelled_collaborations = []

            raw_collaborations = [a_tuple[0] for a_tuple in labelled_collaborations]  #

            if labelled_genres is None:
                labelled_genres = []

            raw_genres = [a_tuple[0] for a_tuple in labelled_genres]  #

            if labelled_alt_titles is None:
                labelled_alt_titles = []

            raw_alts = [a_tuple[0] for a_tuple in labelled_alt_titles]  #

            MeraMusicalEntity.__init__(self,
                                       labelled_canonical=labelled_canonical)

            Song.__init__(self,
                          canonical=labelled_canonical[0],
                          artists=artists,
                          collaborations=raw_collaborations,
                          duration=duration,
                          genres=raw_genres,
                          release_date=release_date,
                          album=album,
                          alt_titles=raw_alts,
                          country=labelled_country[0] if labelled_country is not None else None,
                          discogs_id=discogs_id,
                          discogs_index=discogs_index,
                          usos_isrc=usos_isrc,
                          usos_transaction_id=usos_transaction_id,
                          iswc=iswc)

            self._labelled_alt_titles = labelled_alt_titles
            self._labelled_country = labelled_country
            self._labelled_genres = labelled_genres
            self._labelled_collaborations = labelled_collaborations

    @property
    def collaborations_tuples(self):
        for a_tuple in self._labelled_collaborations:
            yield a_tuple

    def add_collaboration(self, labelled_collaboration):
        super(MeraSong, self).add_collaboration(labelled_collaboration[0])
        self._labelled_collaborations.append(labelled_collaboration)

    @property
    def genres_tuples(self):
        for a_tuple in self._labelled_genres:
            yield a_tuple

    def add_genre(self, labelled_genre):
        super(MeraSong, self).add_genre(labelled_genre[0])
        self._labelled_genres.append(labelled_genre)


    @property
    def alternative_titles_tuples(self):
        for a_tuple in self._labelled_alt_titles:
            yield a_tuple

    def add_alternative_title(self, labelled_title):
        super(MeraSong, self).add_alternative_title(labelled_title[0])
        self._labelled_alt_titles.append(labelled_title)


    @property
    def country_source(self):
        return None if self._labelled_country is None else self._labelled_country[1]

    @property
    def country_tuple(self):
        return self._labelled_country


    @property
    def identifying_form_tuples(self):
        yield self._labelled_canonical
        for title in self._labelled_alt_titles:
            yield title

    @property
    def identifying_forms(self):
        yield self._canonical
        for title in self._alt_titles:
            yield title


class MeraArtist(Artist, MeraMusicalEntity):
    def __init__(self, labelled_canonical, labelled_aliases=None, labelled_namevars=None,
                 labelled_country=None, discogs_id=None):
        """

        :param labelled_canonical:
        :param labelled_aliases:
        :param labelled_namevars:
        :param labelled_country:
        :return:
        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if MeraArtist not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(MeraArtist)
            # print "MeraArtist", labelled_canonical
            if labelled_namevars is None:
                labelled_namevars = []

            if labelled_aliases is None:
                labelled_aliases = []

            raw_aliases = [a_tuple[0] for a_tuple in labelled_aliases]
            raw_namevars = [a_tuple[0] for a_tuple in labelled_namevars]
            raw_country = None if labelled_country is None else labelled_country[0]

            MeraMusicalEntity.__init__(self,
                                       labelled_canonical=labelled_canonical)
            Artist.__init__(self,
                            canonical=labelled_canonical[0],
                            aliases=raw_aliases,
                            namevars=raw_namevars,
                            country=raw_country,
                            discogs_id=discogs_id)


            self._labelled_aliases = labelled_aliases
            self._labelled_country = labelled_country
            self._labelled_namevars = labelled_namevars

    @property
    def identifying_form_tuples(self):
        yield self._labelled_canonical
        for namevar in self._labelled_namevars:
            yield namevar
        for alias in self._labelled_aliases:
            yield alias

    @property
    def identifying_forms(self):
        yield self._canonical
        for namevar in self._namevars:
            yield namevar
        for alias in self._aliases:
            yield alias

    @property
    def namevars_tuples(self):
        for a_labelled_namevar in self._labelled_namevars:
            yield a_labelled_namevar


    @property
    def country_source(self):
        return self._labelled_country[1] if self._labelled_country is not None else None

    @property
    def country_tuple(self):
        return self._labelled_country


    def add_namevar(self, namevar):
        """
        It expects a tuple with the namevar in the first pos and the source in the second one
        :param namevar:
        :return:
        """
        super(MeraArtist, self).add_namevar(namevar[0])
        self._labelled_namevars.append(namevar)


    @property
    def aliases_tuples(self):
        for alias in self._labelled_aliases:
            yield alias


    def add_alias(self, alias):
        """
        It expects a tuple with the alias in the first pos and the source in the second one
        :param alias:
        :return:
        """
        super(MeraArtist, self).add_alias(alias[0])
        self._labelled_aliases.append(alias)


class MeraArtistPerson(ArtistPerson, MeraArtist):
    def __init__(self, labelled_canonical, labelled_civil=None,
                 labelled_aliases=None, labelled_namevars=None, labelled_country=None, discogs_id=None):
        """

        :param labelled_canonical:
        :param labelled_civil:
        :param labelled_aliases:
        :param labelled_namevars:
        :param labelled_country:
        :return:
        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if MeraArtistPerson not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(MeraArtistPerson)
            # print "MeraArtistPerson", labelled_canonical
            if labelled_namevars is None:
                labelled_namevars = []

            if labelled_aliases is None:
                labelled_aliases = []

            raw_aliases = [a_tuple[0] for a_tuple in labelled_aliases]
            raw_namevars = [a_tuple[0] for a_tuple in labelled_namevars]
            raw_country = None if labelled_country is None else labelled_country[0]
            raw_civil = None if labelled_civil is None else labelled_civil[0]

            MeraArtist.__init__(self,
                                labelled_canonical=labelled_canonical,
                                labelled_aliases=labelled_aliases,
                                labelled_namevars=labelled_namevars,
                                labelled_country=labelled_country,
                                discogs_id=discogs_id)
            ArtistPerson.__init__(self,
                                  canonical=labelled_canonical[0],
                                  civil=raw_civil,
                                  aliases=raw_aliases,
                                  namevars=raw_namevars,
                                  country=raw_country,
                                  discogs_id=discogs_id)


            self._labelled_civil = labelled_civil

    @property
    def identifying_form_tuples(self):
        yield self._labelled_canonical
        if self._labelled_civil is not None:
            yield self._labelled_civil
        for namevar in self._labelled_namevars:
            yield namevar
        for alias in self._labelled_aliases:
            yield alias


    @property
    def identifying_forms(self):
        yield self._canonical
        if self._civil is not None:
            yield self._civil
        for namevar in self._namevars:
            yield namevar
        for alias in self._aliases:
            yield alias

    @property
    def civil_source(self):
        return self._labelled_civil[1] if self._labelled_civil is not None else None


    @property
    def civil_tuple(self):
        return self._labelled_civil


class MeraArtistGroup(ArtistGroup, MeraArtist):
    def __init__(self, labelled_canonical, labelled_aliases=None, labelled_namevars=None,
                 labelled_country=None, members=None, discogs_id=None):
        """
        :param members: list of ArtistPerson objects

        """
        if TYPE_SET not in self.__dict__:
            self.__dict__[TYPE_SET] = set()
        if MeraArtistGroup not in self.__dict__[TYPE_SET]:
            self.__dict__[TYPE_SET].add(MeraArtistGroup)
            if labelled_namevars is None:
                labelled_namevars = []

            if labelled_aliases is None:
                labelled_aliases = []

            raw_aliases = [a_tuple[0] for a_tuple in labelled_aliases]
            raw_namevars = [a_tuple[0] for a_tuple in labelled_namevars]
            raw_country = None if labelled_country is None else labelled_country[0]


            MeraArtist.__init__(self,
                                labelled_canonical=labelled_canonical,
                                labelled_aliases=labelled_aliases,
                                labelled_namevars=labelled_namevars,
                                labelled_country=labelled_country,
                                discogs_id=discogs_id)

            ArtistGroup.__init__(self,
                                 canonical=labelled_canonical[0],
                                 aliases=raw_aliases,
                                 namevars=raw_namevars,
                                 country=raw_country,
                                 members=members,
                                 discogs_id=discogs_id)




    @property
    def identifying_form_tuples(self):
        yield self._labelled_canonical
        for namevar in self._labelled_namevars:
            yield namevar
        for alias in self._labelled_aliases:
            yield alias
        for member in self._members:
            for form in member.identifying_form_tuples:
                yield form  # Sure oh this?? We may be giving advantage to groups over artist


    @property
    def identifying_forms(self):
        yield self._canonical
        for namevar in self._namevars:
            yield namevar
        for alias in self._aliases:
            yield alias
        for member in self._members:
            for form in member.identifying_forms:
                yield form
