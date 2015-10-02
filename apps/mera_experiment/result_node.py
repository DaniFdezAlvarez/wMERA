__author__ = 'Dani'


MISSING = -1


class ExperimentResultNode(object):


    def __init__(self, list_of_mera_base_results, target_id, song, artists, writers):
        self._list_of_mera_base_results = list_of_mera_base_results
        self._target_id = target_id
        self._song = song
        self._artists = artists
        self._writers = writers

    @property
    def sorted_mera_results(self):
        for a_res in self._list_of_mera_base_results:
            yield a_res

    @property
    def number_of_results(self):
        return len(self._list_of_mera_base_results)

    @property
    def target_id(self):
        return self._target_id

    @property
    def song(self):
        return self._song

    @property
    def artists(self):
        for artist in self._artists:
            yield artist

    @property
    def writers(self):
        for writer in self._writers:
            yield writer

    @property
    def query_str(self):
        result = self._song + "\t"
        for an_art in self._artists:
            result += an_art + "|"
        for a_wri in self._writers:
            result += a_wri + "|"
        return result

    @property
    def target_id_classification(self):
        counter = 1
        for a_mera_result in self._list_of_mera_base_results:
            if a_mera_result.entity.discogs_id == self._target_id:
                return counter
            counter += 1
        return MISSING

    @property
    def target_id_score(self):
        for a_mera_result in self._list_of_mera_base_results:
            if a_mera_result.entity.discogs_id == self._target_id:
                return a_mera_result.get_max_score()
        return MISSING

    @property
    def no_target_id_better_score(self):
        for a_mera_result in self._list_of_mera_base_results:
            if a_mera_result.entity.discogs_id != self._target_id:
                return a_mera_result.get_max_score()
        return 0
