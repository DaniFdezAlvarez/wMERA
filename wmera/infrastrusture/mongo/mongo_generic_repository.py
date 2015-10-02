__author__ = 'Dani'

from wmera.infrastrusture.mongo.config import host, port, db_name
from wmera.infrastrusture.mongo.mongo_connection import connect_to_db


class MongoGenericRepository(object):
    ELEMENTS_PER_PAGE = 15

    def __init__(self, url_root, collection, new_host=None, new_port=None):

        target_host = host if new_host is None else new_host
        target_port = port if new_port is None else new_port
        self._db = connect_to_db(host=target_host, port=target_port, db_name=db_name)
        self._url_root = url_root
        self._collection = collection

    @property
    def collection(self):
        return self._collection

    def find_all(self, page_number):
        return list(self._db[self.collection].find().skip(int(page_number) * self.ELEMENTS_PER_PAGE).limit(
            self.ELEMENTS_PER_PAGE))

    def find_by_id(self, item_id):
        item = self._db[self.collection].find_one({'_id': item_id})

        if item is None:
            return "The item with id {} was not found in collection {}".format(item_id, self.collection)

        return item

    def insert_items(self, items):
        for item in items:
            self.insert_item(item)

    def insert_item(self, item):
        self._db[self.collection].insert(item.to_mongo_dict())

    def drop_collection(self):
        self._db[self.collection].drop()