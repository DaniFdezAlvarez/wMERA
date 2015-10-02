__author__ = 'Dani'

from rdflib import Namespace, URIRef

base_entities_URI = "http://example.org/nuestras_entidades/"
base_properties_URI = "http://example.org/nuestras_propiedades/"
base_types_URI = "http://example.org/nuestros_tipos/"

went = Namespace(base_entities_URI)
wtyp = Namespace(base_types_URI)
wpro = Namespace(base_properties_URI)
mo = Namespace("http://purl.org/ontology/mo/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
tl = Namespace("http://purl.org/NET/c4dm/timeline.owl#")
event = Namespace("http://purl.org/NET/c4dm/event.owl#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")


def bind_namespaces(graph):
    """
    Binds URIs with their correspondings prefixes
    :param graph:
    :return:
    """

    n_space = {"went": went, "wtyp": wtyp, "wpro": wpro,
               "mo": mo, "dc": dc, "xsd": xsd, "tl": tl,
               "event": event, "owl": owl, "foaf": foaf,
               "rdfs": rdfs, "rdf": rdf}

    for prefix, uri in n_space.items():
        graph.namespace_manager.bind(prefix, URIRef(Namespace(uri)))


class MO(object):
    music_artist = mo.term("MusicArtist")
    music_group = mo.term("MusicGroup")
    publishing_location = mo.term("publishing_location")  # Only for works
    origin = mo.term("origin")  # Only for artist
    track = mo.term("Track")
    member = mo.term("member")


class WPRO(object):
    source = wpro.term("source")
    civil_name = wpro.term("civil_name")
    alias = wpro.term("alias")
    namevar = wpro.term("namevar")
    alternative_title = wpro.term("alternative_title")
    entity_target = wpro.term("entity_target")
    download_link = wpro.term("download_link")
    home_page = wpro.term("homepage")
    discogs_id = wpro.term("discogs_id")
    discogs_index = wpro.term("discogs_index")
    usos_transaction_id = wpro.term("usos_transaction_id")
    usos_isrc = wpro.term("usos_isrc")


class WTYP(object):
    str_labelled = wtyp.term("Str_labelled")
    entity_labelled = wtyp.term("Entity_labelled")
    source = wtyp.term("Source")


class DC(object):
    title = dc.term("title")


