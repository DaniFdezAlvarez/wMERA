__author__ = 'Dani'


class MeraFormaterInterface(object):

    def format_mera_results(self, list_of_dicts_with_list_of_base_results):
        raise NotImplementedError()

    def format_mera_result(self, list_of_base_results):
        raise NotImplementedError()




