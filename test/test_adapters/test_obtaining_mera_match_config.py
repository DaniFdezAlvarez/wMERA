__author__ = 'Dani'

import unittest
import json

from wmera.utils import rel_path_to_file
from wmera.mera_core.mera_matcher.json_to_match_config import translate_json_to_mera_match_config


class TestObtainingMeraMatchConfig(unittest.TestCase):
    def test_json_to_mera_match_config(self):
        with open(rel_path_to_file(rel_path="../../files/usos/base_config.json",
                                   base_file=__file__), "r") as json_source:
            source_content = json.load(json_source)
        config_result = translate_json_to_mera_match_config(source_content)

        self.assertEquals(0.65, config_result.get_minimum_of_type("artist"))
        self.assertEquals(0.65, config_result.get_minimum_of_type("song"))

        self.assertEquals(40, config_result.top_k_blocking_function())
        self.assertEquals(5, config_result.top_k_results())

        self.assertEquals(1.60, config_result.get_command_threshold("find_song"))
        self.assertEquals(0.80, config_result.get_command_relevance_of_a_type(command_name="find_song",
                                                                              target_type="artist"))

