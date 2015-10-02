# coding=utf-8
from wmera.mera_core.model.entities import ArtistPerson, Song, Artist, Collaboration, ArtistGroup, ROLE_WRITER
from wmera.parsers.interface.artist_parser_interface import ArtistParserInterface
from wmera.parsers.interface.song_parser_interface import SongParserInterface

__author__ = 'Dani'


class FakeArtistParser(ArtistParserInterface):
    def parse_artists(self):
        yield (ArtistPerson(canonical="Shakira",
                            civil="Shakira Isabel Mebarack Ripoll",
                            aliases=["Shaki", "Shikira"],
                            country="Colombia"))

        yield (ArtistPerson(canonical="Enrique Iglesias",
                            civil="Enrique Iglesias Puga",
                            namevars=["Enrique Iglesias JR", "Enriquito"],
                            country="Spain"))


class FakeRepeatedArtistsParser(ArtistParserInterface):

    def parse_artists(self):
        yield(ArtistPerson(canonical="Shakira",
                           civil="Shakira Isabel Mebarack Ripoll",
                           aliases=["Shaki", "Shikira"],
                           country="Colombia"))

        yield(ArtistPerson(canonical="Enrique Iglesias",
                           civil="Enrique Iglesias Puga",
                           namevars=["Enrique Iglesias JR", "Enriquito"],
                           country="Spain"))

        yield(ArtistPerson(canonical="Shakira",  # Entity repeated exactly
                           civil="Shakira Isabel Mebarack Ripoll",
                           aliases=["Shaki", "Shikira"],
                           country="Colombia"))

        yield(ArtistPerson(canonical="Enrique Iglesias Puga",  # Canonical is the same of civil
                           namevars=["Enrique Iglesias JR", "Enricolancio"],  # One is the same, the other is different
                           country="Spain"))


class FakeRepeatedSongParser(SongParserInterface):
    def parse_songs(self):

        yield Song(canonical="ABCEDE",
                   artists=[ArtistPerson(canonical="Perry Mason",
                                         civil="Perry James Mason")],
                   country="Peru")  # # utf-8 ;)

        yield Song(canonical="Avaloncho",
                   artists=[Artist(canonical="Herroes del selencio")])

        yield Song(canonical="Avalincho",
                   artists=[Artist(canonical="Herroes del selencio",
                                   namevars=["Enrique Bunbury y colegas"])])


class FakeSongParser(SongParserInterface):

    def parse_songs(self):
        yield Song(canonical="Amor de verano",
                   artists=[ArtistPerson(canonical="Perry Mason",
                                         civil="Perry James Mason"),
                            ArtistGroup(canonical="Iggy Azazela")],
                   collaborations=[Collaboration(role=ROLE_WRITER,
                                                 collaborator=ArtistPerson(canonical="Escribano Gonzalez")),
                                   Collaboration(role=ROLE_WRITER,
                                                 collaborator=Artist(canonical="MaripiLampito"))],
                   duration="2:15",
                   genres=["Pop", "Rock"],
                   release_date="",
                   album="Amores en estaciones",
                   alt_titles=["Amr de verno", "Amor de verano MAXIMO"],
                   country="China")

        yield Song(canonical="ABCEDE",
                   artists=[ArtistPerson(canonical="Perry Mason",
                                         civil="Perry James Mason")],
                   country="Peru")  # # utf-8 ;)

        yield Song(canonical="Avaloncho",
                   artists=[Artist(canonical="Herroes del selencio")])

        yield Song(canonical="Avalincho",
                   artists=[ArtistPerson(canonical="Perry Mason",
                                         civil="Perry James Mason")])

