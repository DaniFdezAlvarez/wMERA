__author__ = 'Dani'


from wmera.mera_core.mera_matcher.match_config import MeraMatchConfig

# Types and orders
ORDER_FIND_SONG = 'find_song'
ORDER_FIND_ARTIST = 'find_artist'

TYPE_SONG = 'song'
TYPE_ARTIST = 'artist'


# Main keys
BLOCKING = 'blocking'
COMMANDS = 'commands'
FIELDS = 'fields'


#Blocking keys
TOP_K_BLOCKING_FUNCTION = 'blocking_function'
TOP_K_RESULT = 'result_query'


#Commadn keys
THRESHOLD = 'threshold'
RELEVANCES = 'relevances'



def translate_json_to_mera_match_config(config_dict):

    # Initialize and blocking
    result = MeraMatchConfig(top_k_block=config_dict[BLOCKING][TOP_K_BLOCKING_FUNCTION],
                             top_k_result=config_dict[BLOCKING][TOP_K_RESULT])
    # Commands
    for command_key in config_dict[COMMANDS]:
        command_dict = config_dict[COMMANDS][command_key]
        result.add_command(command_name=command_key, threshold=command_dict[THRESHOLD])
        for a_field_name in command_dict[RELEVANCES]:
            result.add_type_to_command(command_name=command_key,
                                       target_type=a_field_name,
                                       relevance=command_dict[RELEVANCES][a_field_name])

    # Minimums
    for type_key in config_dict[FIELDS]:
        result.add_minimum(target_type=type_key,
                           minimum=config_dict[FIELDS][type_key][THRESHOLD])

    return result

    # TODO Complete with algorithm selection
