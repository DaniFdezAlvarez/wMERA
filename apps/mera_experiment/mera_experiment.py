__author__ = 'Dani'

# from apps.mera_experiment.query_gen.aol_query_gen import AolQueryGen
# from apps.mera_experiment.query_gen.musicbrainz_query_gen import MusicbrainzQueryGen
from apps.mera_experiment.result_node import MISSING

import json


SIXTH_OR_WORSE = 6


class MeraExperiment(object):
    def __init__(self, query_gen, description):
        self._query_gen = query_gen
        self._description = description


    def run(self):
        # aol_result_nodes = AolQueryGen(matcher=self._matcher,
        #                                aol_path_file=self._aol_file).run_queries()
        # musicbrainz_result_nodes = MusicbrainzQueryGen(matcher=self._matcher,
        #                                                musicbrainz_path_file=self._musicbrainz_file).run_queries()
        # aol_result_str = self._process_results(aol_result_nodes)
        # musicbrainz_result_str = self._process_results(musicbrainz_result_nodes)

        # return "AOL summary: \n" + aol_result_str[0] + "\nMB summary:\n" + musicbrainz_result_str[0] \
        # + "\n\n---------\n\n" + "\nAOL verbose:\n" + aol_result_str[1] \
        #        + "\n\n------------\n\nMB verbose:\n" + musicbrainz_result_str[1]
        result_nodes = self._query_gen.run_queries()
        return self._process_results(result_nodes)



    def _process_results(self, result_nodes):
        """
        Return a tuple ("summary", complex result"), both str
        :return:
        """
        result_nodes_list = list(result_nodes)
        summary_rate_dict, whole_rate_str = self._result_nodes_rating(result_nodes_list)
        summary_distance_dict, whole_distance_str = self._result_nodes_distances(result_nodes_list)
        return ExperimentResult(description=self._description,
                                dict_ratings=summary_rate_dict,
                                dict_average_distances=summary_distance_dict,
                                ratings_str=whole_rate_str,
                                distances_str=whole_distance_str,
                                num_results=len(result_nodes_list))


    def _result_nodes_distances(self, result_nodes):
        average_distances_dict = {}
        denominator_averages_dict = {}
        whole_distances_str = "All distances:\n\n"

        for i in range(1, 6):
            average_distances_dict[i] = 0
            denominator_averages_dict[i] = 0
        average_distances_dict[MISSING] = 0
        average_distances_dict[SIXTH_OR_WORSE] = 0
        denominator_averages_dict[SIXTH_OR_WORSE] = 0

        for r_node in result_nodes:
            # Calculating distance averages
            qualifying = r_node.target_id_classification
            qualifying_score = r_node.target_id_score
            better_no_qualifying_score = r_node.no_target_id_better_score

            if qualifying == 1:
                average_distances_dict[1] = self._calculate_new_average(current=average_distances_dict[1],
                                                                        denominators=denominator_averages_dict,
                                                                        denominator_key=1,
                                                                        new_value_high=qualifying_score,
                                                                        new_value_low=better_no_qualifying_score)
            elif qualifying == MISSING:
                pass  # Infinite distance, whit the data we have
            elif qualifying >= 6:
                average_distances_dict[SIXTH_OR_WORSE] = self._calculate_new_average(
                    current=average_distances_dict[SIXTH_OR_WORSE],
                    denominators=denominator_averages_dict,
                    denominator_key=SIXTH_OR_WORSE,
                    new_value_high=better_no_qualifying_score,
                    new_value_low=qualifying_score)
            else:  # qualifying in [2-5]
                average_distances_dict[qualifying] = self._calculate_new_average(
                    current=average_distances_dict[qualifying],
                    denominators=denominator_averages_dict,
                    denominator_key=qualifying,
                    new_value_high=better_no_qualifying_score,
                    new_value_low=qualifying_score)

            # Doing r_node summary
            if qualifying == MISSING:
                whole_distances_str += "-  " + r_node.query_str + ": Missing query, no distance\n"
            elif qualifying == 1:
                if better_no_qualifying_score == MISSING:
                    whole_distances_str += "-  " + r_node.query_str + ": Qualified first, no alternatives.\n"
                else:
                    whole_distances_str += "-  " + r_node.query_str + ": Qualified first. Target: " + str(
                        qualifying_score) + ". 2nd: " + str(better_no_qualifying_score) + ". \n"
            else:
                whole_distances_str += "-  " + r_node.query_str + ": Qualified " + str(qualifying) + ". Target: " + str(
                    qualifying_score) + ". 1st: " + str(better_no_qualifying_score) + ". \n"

        # Returning results
        return average_distances_dict, whole_distances_str


    @staticmethod
    def _calculate_new_average(current, denominators, denominator_key, new_value_high, new_value_low):
        if new_value_high == 0 or new_value_low == 0:
            return current
        result = (current * denominators[denominator_key] + (new_value_high / new_value_low - 1)) / \
                 (denominators[denominator_key] + 1)
        denominators[denominator_key] += 1
        return result


    def _result_nodes_rating(self, result_nodes):
        summary_rate_dict = {}
        summary_rate_str = ""
        for i in range(1, 6):
            summary_rate_dict[i] = 0
        summary_rate_dict[MISSING] = 0
        summary_rate_dict[SIXTH_OR_WORSE] = 0
        for r_node in result_nodes:
            qualifying = r_node.target_id_classification
            if qualifying >= 6:
                summary_rate_dict[SIXTH_OR_WORSE] += 1
            elif qualifying == MISSING:
                summary_rate_dict[MISSING] += 1
            else:
                summary_rate_dict[qualifying] += 1

            # ###
            if qualifying == 1:
                summary_rate_str += "- " + r_node.query_str + ": 1st OK\n"
            else:
                if qualifying == MISSING:
                    summary_rate_str += "- " + r_node.query_str + ": MISSED\n"
                    counter = 0
                    for a_res in r_node.sorted_mera_results:
                        counter += 1
                        summary_rate_str += "\t" + str(counter) + ": " + self._summ_str_of_base_result(a_res) + "\n"
                else:
                    summary_rate_str += "- " + r_node.query_str + ": position " + str(qualifying) + "\n"
                    counter = 0
                    for a_res in r_node.sorted_mera_results:
                        counter += 1
                        if counter == qualifying:
                            break
                        summary_rate_str += "\t" + str(counter) + ": " + self._summ_str_of_base_result(a_res) + "\n"

        return summary_rate_dict, summary_rate_str


    @staticmethod
    def _summ_str_of_base_result(base_result):
        discogs_id_str = base_result.entity.discogs_id if base_result.entity.discogs_id is not None else "UNKNOWN"
        return base_result.entity.canonical + "  " + discogs_id_str \
               + "  " + str(base_result.get_max_score())


# #####################################################################################################


ORDERED_REPORT_KEYS = [1, 2, 3, 4, 5, SIXTH_OR_WORSE, MISSING]


class ExperimentResult(object):
    def __init__(self, description, dict_ratings, dict_average_distances, ratings_str, distances_str, num_results):
        self._description = description
        self._ratings = dict_ratings
        self._distance_averages = dict_average_distances
        self._ratings_str = ratings_str
        self._distances_str = distances_str
        self._num_results = num_results


    @staticmethod
    def _text_classified(a_key):
        if a_key == 1:
            return "1st"
        elif a_key == 2:
            return "2nd"
        elif a_key == 3:
            return "3rd"
        elif a_key in [4, 5]:
            return str(a_key) + "th"
        elif a_key == MISSING:
            return "MISSING"
        else:
            return "SIX OR WORSE"


    @property
    def size(self):
        return self._num_results

    @property
    def ratings(self):
        return self._ratings

    @property
    def distances(self):
        return self._distance_averages

    @property
    def rating_report(self):
        result = "RATING REPORT:\n\n"
        result += "Summary:\n"
        for key in ORDERED_REPORT_KEYS:
            result += "Clasiffied " + self._text_classified(key) + ": " + str(self._ratings[key]) + "\n"
        result += "\nRating per each query:\n\n"
        result += self._ratings_str
        return result

    @property
    def distances_report(self):
        result = "RATING REPORT:\n\n"
        result += "Summary:\n"
        for key in ORDERED_REPORT_KEYS:
            if key in self.distances:
                result += "Average distance to better non-target element. Clasiffied " + self._text_classified(
                    key) + ": " + str(self._distance_averages[key]) + "\n"
        result += "\nDistances per each query:\n\n"
        result += self._distances_str
        return result

    @property
    def report(self):
        result = "MERA EXPERIMENT: " + self._description + "\n\n"
        result += "SUMMARY:\n-------\n\n"
        result += str(self._num_results) + " queries run.\n\n"
        result += "Rating Summary:\n"
        for key in ORDERED_REPORT_KEYS:
            result += "Clasiffied " + self._text_classified(key) + ": " + str(self._ratings[key]) + "\n"
        result += "\nDistances summary:\n"
        for key in ORDERED_REPORT_KEYS:
            if key in self.distances:
                result += "Average distance to better non-target element. Clasiffied " + self._text_classified(
                    key) + ": " + str(self._distance_averages[key]) + "\n"

        result += "RATING FOR EACH QUERY:\n\n"
        result += self._ratings_str
        result += "\n\nDISTANCE FOR EACH QUERY:\n\n"
        result += self._distances_str
        return result


    def serialize_experiment(self, file_path):
        with open(file_path, "w") as file_io:
            json.dump(self.__dict__, file_io)


    def load_experiment(self, file_path):
        with open(file_path, "r") as file_io:
            self.__dict__ = json.load(file_io)


    def report_to_file(self, file_path):
        with open(file_path, "w") as file_io:
            file_io.write(self.report)