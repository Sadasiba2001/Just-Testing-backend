# mongo_connection.py
from pymongo import MongoClient
from django.conf import settings

class MongoDBConnection:
    def __init__(self):
        self.client = MongoClient(settings.DATABASES['default']['HOST'])
        self.db = self.client[settings.DATABASES['default']['NAME']]

    def get_collection(self, collection_name):
        return self.db[collection_name]
