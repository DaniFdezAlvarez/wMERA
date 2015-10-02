__author__ = 'Dani'

# CONST_NAMES
_THRESHOLD = 'threshold'
_RELEVANCES = 'relevances'


class MeraMatchConfig(object):
    def __init__(self, top_k_block=60, top_k_result=15):
        # # Top k's
        self._top_k_block = top_k_block
        self._top_k_result = top_k_result

        self._minims_of_type = {}
        self._commands = {}

        ## Defaults
        self._default_threshold = 1  # Should be configurable
        self._default_generic_relevance = 0.80  # Should be configurable
        self._default_minimum = 0.60
        self._default_relevance_of_types = {}




    def top_k_blocking_function(self):
        return self._top_k_block


    def top_k_results(self):
        return self._top_k_result


    def add_command(self, command_name, threshold=None, relevance_tuples_list=None):
        """

        :param command_name:
        :param threshold:
        :param relevance_tuples_list: expected to be a list of tuples in which the firts position is
        a type and the second one is the relevance of the type when processing this concrete order.
        :return:
        """
        # Initializing
        if command_name in self._commands:
            return  # Some kind of error, but lets be zen
        self._commands[command_name] = {}

        # Threshold
        if threshold is not None:
            self._commands[command_name][_THRESHOLD] = threshold
        else:
            self._commands[command_name][_THRESHOLD] = self._default_threshold

        #relevances
        self._commands[command_name][_RELEVANCES] = {}
        if relevance_tuples_list is not None:
            for a_tuple in relevance_tuples_list:
                self._commands[command_name][_RELEVANCES][a_tuple[0]] = a_tuple[1]

    def add_type_to_command(self, command_name, target_type, relevance):
        if command_name not in self._commands:
            return  # Some kind of error, but live and let live
        self._commands[command_name][_RELEVANCES][target_type] = relevance

    def get_command_threshold(self, command_name):
        if command_name not in self._commands:
            return self._default_threshold
        else:
            return self._commands[command_name][_THRESHOLD]


    def get_command_relevance_of_a_type(self, command_name, target_type):
        rev_in_failure = self._default_generic_relevance if target_type not in self._default_relevance_of_types else \
            self._default_relevance_of_types[target_type]
        if command_name not in self._commands:
            return rev_in_failure
        elif target_type not in self._commands[command_name]:
            return rev_in_failure
        else:
            return self._commands[command_name][target_type]

    def get_minimum_of_type(self, target_type):
        if target_type not in self._minims_of_type:
            return self._default_minimum
        else:
            return self._minims_of_type[target_type]

    def add_minimum(self, target_type, minimum):
        self._minims_of_type[target_type] = minimum





