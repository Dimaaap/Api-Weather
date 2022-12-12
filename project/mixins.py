from os import getenv

from pymongo import MongoClient


class ConnectToMongoMixin:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client['cities_weather']