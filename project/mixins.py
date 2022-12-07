from os import getenv

from pymongo import MongoClient


class ConnectToMongoMixin:

    def __init__(self):
        self.client = MongoClient(getenv('MONGO_HOST'), int(getenv('MONGO_PORT')))
        self.database = self.client['cities_weather']