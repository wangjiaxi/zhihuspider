from pymongo import MongoClient
from pymongo import errors
from logging import warning
class Mongo(object):
    def __init__(self, host='localhost', port=27017, db_name=None):
        try:
            client = MongoClient(host, port)
        except errors.ConnectionFailure as e:
            warning(e)
        self.db = client['db_name']
        self.collection = None

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def insert_many(self, data):
        return self.collection.insert_many(data)

    def find_one(self, data):
        return self.collection.find_one(data)

