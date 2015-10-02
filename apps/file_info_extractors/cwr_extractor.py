__author__ = 'Dani'

from wmera.infrastrusture.mongo.cwr.work_repository import WorkRepository


class CwrExtarctor(object):

    def __init__(self, url_root):
        self._repository = WorkRepository(url_root=url_root)


    def get_ramdom_writers_names(self, num_writers=100):
        return self._repository.find_random_writer_names(num_writers)