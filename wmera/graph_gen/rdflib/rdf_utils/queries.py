__author__ = 'Dani'

from rdflib.plugins.sparql import prepareQuery

# ####### ARTIST

# Canonical
_FIND_CANONICAL_BEGIN = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " \
                        "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                        "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>" \
                        "SELECT ?canonical ?source WHERE { <"
_FIND_CANONICAL_END = "> foaf:name ?lab_entity . ?lab_entity rdfs:label ?canonical; wpro:source ?source . }"

# Aliases
_FIND_ALIASES_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                      "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> " \
                      "SELECT ?alias ?source WHERE { <"
_FIND_ALIASES_END = "> wpro:alias ?lab_str . ?lab_str rdfs:label ?alias;  wpro:source ?source. }"

# Namevars
_FIND_NAMEVARS_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                       "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> " \
                       "SELECT ?namevar ?source WHERE { <"
_FIND_NAMEVARS_END = "> wpro:namevar ?lab_str . ?lab_str rdfs:label ?namevar;  wpro:source ?source. }"

# Artist_country
_FIND_COUNTRY_BEGIN = "PREFIX mo: <http://purl.org/ontology/mo/> " \
                      "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                      "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>  " \
                      "SELECT ?country ?source WHERE { <"
_FIND_COUNTRY_END = "> mo:origin ?lab_entity . ?lab_entity wpro:entity_target ?country_entity; wpro:source ?source." \
                    " ?country_entity rdfs:label ?country }"

# Civil
_FIND_CIVIL_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                    "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> " \
                    "SELECT ?civil ?source WHERE { <"
_FIND_CIVIL_END = "> wpro:civil ?lab_str . ?lab_str rdfs:label ?civil;  wpro:source ?source. }"

# Group_members (just one field per row)
_FIND_MEMBERS_BEGIN = "PREFIX mo: <http://purl.org/ontology/mo/> SELECT ?uri_member WHERE { <"
_FIND_MEMBERS_END = "> mo:member ?uri_member . }"



# ###### SONGS

#Artist uri
_FIND_ARTISTS_BEGIN = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " \
                      "PREFIX mo: <http://purl.org/ontology/mo/>" \
                      "SELECT ?uri_artist WHERE { <"
_FIND_ARTISTS_END = "> foaf:maker ?uri_artist . }"


#Compiler uri
_FIND_COMPILER_BEGIN = "PREFIX mo: <http://purl.org/ontology/mo/> " \
                       "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                       "SELECT ?uri_person ?uri_source WHERE { <"
_FIND_COMPILER_END = "> mo:compiler ?lab_entity . ?lab_entity wpro:source ?uri_source ;" \
                     " wpro:entity_target ?uri_person . }"

#Genres (name)

_FIND_GENRES_BEGIN = "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> " \
                     "PREFIX mo: <http://purl.org/ontology/mo/> " \
                     "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                     "SELECT ?genre_label ?uri_source WHERE { <"
_FIND_GENRES_END = "> mo:genre ?lab_entity . ?lab_entity wpro:source ?uri_source ; wpro:entity_target ?uri_genre . " \
                   "?uri_genre rdfs:label ?genre_label . }"

#Alt_titles

_FIND_ALT_TITLES_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                         "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> " \
                         "SELECT ?alt_title ?source WHERE { <"
_FIND_ALT_TITLES_END = "> wpro:alternative_title ?lab_str . ?lab_str rdfs:label ?alt_title;  wpro:source ?source. }"


#Discogs_ID

_FIND_DISCOGS_ID_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> SELECT ?discogs_id WHERE { <"
_FIND_DISCOGS_ID_END = "> wpro:discogs_id ?discogs_id . }"


#Discogs_index

_FIND_DISCOGS_INDEX_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> SELECT ?discogs_index WHERE { <"
_FIND_DISCOGS_INDEX_END = "> wpro:discogs_index ?discogs_index . }"

#USOS transaction id

_USOS_TRANSACTION_ID_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> SELECT ?usos_tr_id WHERE { <"
_USOS_TRANSACTION_ID_END = "> wpro:usos_transaction_id ?usos_tr_id . }"


#USOS isrc

_USOS_ISRC_BEGIN = "PREFIX wpro: <http://example.org/nuestras_propiedades/> SELECT ?usos_isrc WHERE { <"
_USOS_ISRC_END = "> wpro:usos_isrc ?usos_isrc . }"



### MERGING

#Intermediary entity for text
_FIND_INTERMEDIARY_URI_TEXT_P1 = "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> " \
                                 " SELECT ?intermediary_uri WHERE { <"
_FIND_INTERMEDIARY_URI_TEXT_P2 = "> <"
_FIND_INTERMEDIARY_URI_TEXT_P3 = "> ?intermediary_uri . ?intermediary_uri rdfs:label \""
_FIND_INTERMEDIARY_URI_TEXT_P4 = "\" . }"

#Intermediary entity for target entity
_FIND_INTERMEDIARY_URI_TARGET_ENTITY_P1 = "PREFIX wpro: <http://example.org/nuestras_propiedades/> " \
                                          " SELECT ?intermediary_uri WHERE { <"
_FIND_INTERMEDIARY_URI_TARGET_ENTITY_P2 = "> <"
_FIND_INTERMEDIARY_URI_TARGET_ENTITY_P3 = "> ?intermediary_uri . ?intermediary_uri wpro:entity_target >"
_FIND_INTERMEDIARY_URI_TARGET_ENTITY_P4 = "> . }"



#TODO : RIGHT NOW, not managing album duration and date



class Queries(object):
    ### CANONICAL

    @staticmethod
    def find_canonical_str(musical_entity_uri):
        return _FIND_CANONICAL_BEGIN + musical_entity_uri + _FIND_CANONICAL_END

    @staticmethod
    def find_canonical_compiled(musical_entity_uri):
        return prepareQuery(Queries.find_canonical_str(musical_entity_uri))


    ### ARTIST_COUNTRY

    @staticmethod
    def find_country_str(musical_entity_uri):
        return _FIND_COUNTRY_BEGIN + musical_entity_uri + _FIND_COUNTRY_END

    @staticmethod
    def find_country_compiled(musical_entity_uri):
        return prepareQuery(Queries.find_country_str(musical_entity_uri))


    ### ALIASES

    @staticmethod
    def find_aliases_str(artist_uri):
        return _FIND_ALIASES_BEGIN + artist_uri + _FIND_ALIASES_END

    @staticmethod
    def find_aliases_compiled(artist_uri):
        return prepareQuery(Queries.find_aliases_str(artist_uri))


    ### NAMEVARS

    @staticmethod
    def find_namevars_str(artist_uri):
        return _FIND_NAMEVARS_BEGIN + artist_uri + _FIND_NAMEVARS_END

    @staticmethod
    def find_namevars_compiled(artist_uri):
        return prepareQuery(Queries.find_namevars_str(artist_uri))


    ### CIVIL

    @staticmethod
    def find_civil_str(artisrt_person_uri):
        return _FIND_CIVIL_BEGIN + artisrt_person_uri + _FIND_CIVIL_END

    @staticmethod
    def find_civil_compiled(artist_person_uri):
        return prepareQuery(Queries.find_civil_str(artist_person_uri))


    ### URI_MEMBERS

    @staticmethod
    def find_members_uri_str(artist_group_uri):
        return _FIND_MEMBERS_BEGIN + artist_group_uri + _FIND_MEMBERS_END

    @staticmethod
    def find_members_uri_compiled(artist_gruop_uri):
        return prepareQuery(Queries.find_members_uri_str(artist_gruop_uri))


    ### URI ARTIST OF SONG

    @staticmethod
    def find_artists_uri_str(song_uri):
        return _FIND_ARTISTS_BEGIN + song_uri + _FIND_ARTISTS_END

    @staticmethod
    def find_artists_uri_compiled(song_uri):
        return prepareQuery(Queries.find_artists_uri_str(song_uri))


    ### COMPILER

    @staticmethod
    def find_compiler_uri_str(song_uri):
        return _FIND_COMPILER_BEGIN + song_uri + _FIND_COMPILER_END

    @staticmethod
    def find_compiler_uri_compiled(song_uri):
        return prepareQuery(Queries.find_compiler_uri_str(song_uri))


    ### GENRES

    @staticmethod
    def find_genres_str(song_uri):
        return _FIND_GENRES_BEGIN + song_uri + _FIND_GENRES_END

    @staticmethod
    def find_genres_compiled(song_uri):
        return prepareQuery(Queries.find_genres_str(song_uri))


    ### ALT TITLES

    @staticmethod
    def find_alternative_titles_str(song_uri):
        return _FIND_ALT_TITLES_BEGIN + song_uri + _FIND_ALT_TITLES_END

    @staticmethod
    def find_alternative_titles_compiled(song_uri):
        return prepareQuery(Queries.find_alternative_titles_str(song_uri))


    ### DISCOGS_ID
    @staticmethod
    def find_discogs_id_str(song_uri):
        return _FIND_DISCOGS_ID_BEGIN + song_uri + _FIND_DISCOGS_ID_END

    @staticmethod
    def find_discogs_id_compiled(song_uri):
        return prepareQuery(Queries.find_discogs_id_str(song_uri))


    ### DISCOGS_INDEX
    @staticmethod
    def find_discogs_index_str(song_uri):
        return _FIND_DISCOGS_INDEX_BEGIN + song_uri + _FIND_DISCOGS_INDEX_END

    @staticmethod
    def find_discogs_index_compiled(song_uri):
        return prepareQuery(Queries.find_discogs_index_str(song_uri))

    ### USOS TRANSACTION ID
    @staticmethod
    def find_usos_transaction_id_str(song_uri):
        return _USOS_TRANSACTION_ID_BEGIN + song_uri + _USOS_TRANSACTION_ID_END

    @staticmethod
    def find_usos_transaction_id_compiled(song_uri):
        return prepareQuery(Queries.find_usos_transaction_id_str(song_uri))


    ### USOS ISRC
    @staticmethod
    def find_usos_isrc_str(song_uri):
        return _USOS_ISRC_BEGIN + song_uri + _USOS_ISRC_END

    @staticmethod
    def find_usos_isrc_compiled(song_uri):
        return prepareQuery(Queries.find_usos_isrc_str(song_uri))


    ### INTERMEDIARY URI FOR TEXT
    @staticmethod
    def find_intermediary_uri_for_text_str(primary_entity_uri, primary_property, matching_text):
        return _FIND_INTERMEDIARY_URI_TEXT_P1 + primary_entity_uri + _FIND_INTERMEDIARY_URI_TEXT_P2 + \
               primary_property + _FIND_INTERMEDIARY_URI_TEXT_P3 + matching_text + _FIND_INTERMEDIARY_URI_TEXT_P4

    @staticmethod
    def find_intermediary_uri_for_text_compiled(primary_entity_uri, primary_property, matching_text):
        return prepareQuery(Queries.find_intermediary_uri_for_text_str(primary_entity_uri=primary_entity_uri,
                                                                       primary_property=primary_property,
                                                                       matching_text=matching_text))

    ### INTERMEDIARY URI FOR ENTITY TARGET
    @staticmethod
    def find_intermediary_uri_for_entity_target_str(primary_entity_uri, primary_property, entity_target_uri):
        return _FIND_INTERMEDIARY_URI_TARGET_ENTITY_P1 + primary_entity_uri + \
               _FIND_INTERMEDIARY_URI_TARGET_ENTITY_P2 + primary_property + _FIND_INTERMEDIARY_URI_TARGET_ENTITY_P3 + \
               entity_target_uri + _FIND_INTERMEDIARY_URI_TARGET_ENTITY_P4

    @staticmethod
    def find_intermediary_uri_for_target_entity_compiled(primary_entity_uri, primary_property, entity_target_uri):
        return prepareQuery(Queries.find_intermediary_uri_for_entity_target_str(primary_entity_uri=primary_entity_uri,
                                                                                primary_property=primary_property,
                                                                                entity_target_uri=entity_target_uri))








