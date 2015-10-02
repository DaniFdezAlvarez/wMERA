__author__ = 'Dani'

import json
from wmera.utils import decode_dict
from wmera.graph_gen.rdflib.graph_generator_song_uri_known import GraphGeneratorSongUriKnown
from wmera.parsers.mera_matches.matches_song_uri_known_parser import MatchesSongUriKnownParser

#### Fields oj MJSON

MJSON_TYPE_OF_QUERY = 'type_of_query'
MJSON_MAIN = 'main_info'
MJSON_EXTRA = 'extra_args'

MJSON_WRITER = 'writer'
MJSON_SONG = 'song'
MJSON_ARTIST = 'artist'
MJSON_ALT = 'alt'
MJSON_ALBUM = 'album'
MJSON_ISWC = "iswc"

#### TYPE OF ORDERS
MJSON_ORDER_FIND_SONG = "find_song"





##############################


class QueryExecuter(object):
    def __init__(self, matcher, formater):
        self._matcher = matcher
        self._formater = formater
        pass

    def introduce_json_matches_in_graph(self, json_matches_str, dataset_obj, serialization_path):
        generator_enricher = GraphGeneratorSongUriKnown(mera_graph=self._matcher._graph,
                                                        repo_artist=self._matcher._repo_artist_ngrams,
                                                        repo_songs=self._matcher._repo_song_ngrams,
                                                        repo_counter=self._matcher._repo_counter,
                                                        mera_matcher=self._matcher)
        generator_enricher.run_song_gen(song_parser=MatchesSongUriKnownParser(json_string=json_matches_str,
                                                                              dataset=dataset_obj))
        if serialization_path is not None:
            generator_enricher.write_graph_to_turtle_file(serialization_path)


    def execute_queries_from_json(self, json_content):
        json_queries = self._filter_json_queries(json_content)
        results = []
        q_count = 0
        for a_query in json_queries:
            q_count += 1
            if q_count % 5 == 0:
                print q_count
            a_result = self._execute_query(a_query)
            if a_result is not None:
                results.append({'results': a_result, 'query': a_query})
        return self._formater.format_mera_results(results)

    def execute_queries_from_file(self, file_path):
        """
        Read file, create config objects if needed, invoke one by one the queries, cath the result, format the result
        :param file_path:
        :return:
        """
        return self.execute_queries_from_json(self._parse_json_file(file_path))



    def _execute_query(self, query):
        if query[MJSON_TYPE_OF_QUERY] == MJSON_ORDER_FIND_SONG:
            return self._execute_find_song_query(query)
        return None

    def _execute_find_song_query(self, query):
        name = query[MJSON_MAIN]

        alt_titles = query[MJSON_EXTRA][MJSON_ALT] if MJSON_ALT in query[MJSON_EXTRA] else None

        artist = []
        if MJSON_ARTIST in query[MJSON_EXTRA]:
            artist += query[MJSON_EXTRA][MJSON_ARTIST]
        if MJSON_WRITER in query[MJSON_EXTRA]:
            artist += query[MJSON_EXTRA][MJSON_WRITER]

        album = query[MJSON_EXTRA][MJSON_ALBUM] if MJSON_ALBUM in query[MJSON_EXTRA] else None

        return self._matcher.find_song(name=name,
                                       alt_titles=alt_titles,
                                       artists=artist,
                                       album=album)

    @staticmethod
    def _parse_json_file(file_path):
        with open(file_path, "r") as file_content:
            return json.load(file_content, object_hook=decode_dict)

    @staticmethod
    def _filter_json_queries(json_content):
        return json_content['queries']

    @staticmethod
    def _filter_json_config(json_content):
        return json_content['config']






