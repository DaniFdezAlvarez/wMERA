__author__ = 'Dani'
import json

from wmera.word_utils import extract_ngrams, compare_levenshtein


class MemoryIndex(object):
    def __init__(self):
        self._listdocs = {}
        self._sizedocs = {}
        self._idfs = {}
        self._index = {}
        self._fulltexts = {}
        self._load_index()
        self._load_full_text()
        print "Index fully loaded"


    def find_artist(self, original_query):
        query = original_query.lower().strip()
        results = self._run_query(query)
        best_match = self._get_best_match(query, results)
        return best_match

    def _run_query(self, query, top_k=10):
        result = {}
        ngrams = extract_ngrams(query)
        max_possible_idf = self._calculate_max_possible_idf(ngrams)
        total_tf_idfs = {}
        total_idfs = {}
        for ngram in ngrams:
            if ngram in self._index and ngram in self._idfs:
                candidates = self._index[ngram]
                idf = float(self._idfs[ngram])
                for docid in candidates:
                    if docid not in total_tf_idfs:
                        total_tf_idfs[docid] = 0
                        total_idfs[docid] = 0
                    total_tf_idfs[docid] += candidates[docid] * idf
                    total_idfs[docid] += idf


        for docid in total_idfs:
            if total_idfs[docid] == max_possible_idf:
                name = self._listdocs[docid]
                result[name + "|" + str(docid)] = total_tf_idfs[docid] / self._sizedocs[docid]
                del total_tf_idfs[docid]
        preliminar_results = {}
        for docid in total_tf_idfs:
            name = self._listdocs[docid]
            preliminar_results[name + "|" + str(docid)] = total_tf_idfs[docid] / self._sizedocs[docid]
        preliminar_results = self._get_sorted_highest_results(preliminar_results, top_k)
        for preliminar_key in preliminar_results:
            result[preliminar_key] = preliminar_results[preliminar_key]

        return result

    def _calculate_max_possible_idf(self, ngrams):
        result = 0
        for ngram in ngrams:
            if ngram in self._index and ngram in self._idfs:
                result += float(self._idfs[ngram])
        return result


    @staticmethod
    def _get_sorted_highest_results(target_dict, top_k):
        result = {}

        dict_items = target_dict.items()
        dict_items.sort(key=lambda x: x[1],
                        reverse=True)
        for i in range(0, top_k):
            result[dict_items[i][0]] = dict_items[i][1]

        return result


    def _get_best_match(self, query, candidates, threshold=0.75):
        docid_dict = {}
        for candidate in candidates:
            tmp_arr = candidate.split("|")
            name = tmp_arr[0]
            docid = int(tmp_arr[1])
            docid_dict[docid] = name

        # # We load the full text for all of the candidates
        # # (no, it's not very efficient, a database would be
        # # a better option).
        #
        # with open("../files/fulltext.data", "r") as fulltext_file:
        #     target_fulltexts = {}
        #     max_num = len(candidates)
        #     count = 0
        #     for original_line in fulltext_file:
        #         tmp_arr = original_line.strip().split("\t")
        #         docid = int(tmp_arr[0])
        #         if docid in docid_dict:
        #             target_fulltexts[docid] = json.loads(tmp_arr[1])  # Unserialize this
        #             count += 1
        #             if count == max_num:
        #                 break
        similarities = {}
        for docid in docid_dict:
            similarities[docid] = {}
            for entry in self._fulltexts[docid]:
                if entry.strip() != "":
                    similarity = compare_levenshtein(query, entry.encode("utf-8"))
                    if similarity > threshold:
                        similarities[docid][entry] = similarity

        # We prepare a report from the matches. We are interested in the number
        # of valid matches and the maximum score for the matching against each
        # artist.

        results = {}
        for docid in similarities:
            data = similarities[docid]
            if len(data) not in results and len(data) != 0:
                results[len(data)] = {}
            if len(data) != 0:
                results[len(data)][docid] = max(data.values())
        # Then, we preserve just the documents with the maximum number of matches.
        num_matches = results.keys()
        if len(num_matches) == 0:  # No result was found
            return None
        max_matches = max(num_matches)
        results = results[max_matches]

        # After that, we sort the remaining documents and obtain the one with the
        # largest maching score.

        sorted_results = results.items()
        sorted_results.sort(key=lambda x: x[1], reverse=True)
        best_match = sorted_results[0][0]  # First element, first position of tuple (docid)

        # Finally, we sort the best matches for the candidate artist
        similarities = similarities[best_match]
        # In the next two lines we are creating a list with the keys
        # of similarities ordered by its corresponding value in "similarities"
        sorted_similarity_keys = similarities.items()
        sorted_similarity_keys.sort(key=lambda x: x[1], reverse=True)
        sorted_similarity_keys = [a_tuple[0] for a_tuple in sorted_similarity_keys]

        # Now we just need to return all of the information
        target_fulltexts = self._fulltexts[best_match]
        canonical = target_fulltexts[0]  # The canonical name is the first entry. Yes, it should be a URI.

        matches = {}
        for entry in sorted_similarity_keys:  # Equal to " for entry in similarities, but sorted"
            matches[entry] = similarities[entry]  # Score

        return {
            "query": query,
            "canonical": canonical + "  # It should be n URI",
            "matches": matches
        }


    def _load_full_text(self):
        with open("../files/fulltext.data", "r") as fulltext_file:
            for original_line in fulltext_file:
                tmp_arr = original_line.strip().split("\t")
                docid = int(tmp_arr[0])
                self._fulltexts[docid] = json.loads(tmp_arr[1])  # Unserialize this


    def _load_index(self):
        # We open the index file to load it into main memory
        with open("../files/index.data", "r") as index_file:
            # We load the list of documents with the artists' names (URIs) and
            # the number of associated "documents" (aliases, name variations, etc).

            tmp_line = index_file.readline().strip()
            tmp_line = tmp_line.split("\t")
            for entry in tmp_line:
                tmp_arr = entry.split(":")
                #
                docid = tmp_arr[0]
                name = tmp_arr[1]
                #
                tmp_arr = docid.split("|")
                docid = int(tmp_arr[0])
                numdocs = int(tmp_arr[1])
                #
                self._listdocs[docid] = name
                self._sizedocs[docid] = numdocs

            # Then we load the idf values
            tmp_line = None  # Free memory before reading the next line
            tmp_line = index_file.readline().strip().split("\t")
            for entry in tmp_line:
                tmp_arr = entry.split(":")
                self._idfs[tmp_arr[0]] = tmp_arr[1]

            # Finally we load the index properly
            tmp_line = None  # Free memory
            for tmp_line in index_file:  # Not sure about if the first 2 lines are excluded or not
                tmp_line = tmp_line.strip()
                if tmp_line != "":
                    tmp_line = tmp_line.split("\t")
                    ngram = tmp_line[0]
                    self._index[ngram] = {}
                    for i in range(1, len(tmp_line)):
                        tmp_arr = tmp_line[i].split(":")
                        self._index[ngram][int(tmp_arr[0])] = int(tmp_arr[1])

        





