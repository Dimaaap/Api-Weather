import pytest

from project.mixins import ConnectToMongoMixin
from project.db_wrapper import DbWrapper


@pytest.fixture
def connect_to_db():
    connection = ConnectToMongoMixin()
    test_database = connection.client['test_db']
    test_collection = test_database['test_collection']
    if test_collection.count_documents({}) != 0:
        test_collection.delete_many({})
    yield test_collection
    test_collection.delete_many({})


@pytest.fixture
def insert_data_to_database():
    connection = ConnectToMongoMixin()
    test_database = connection.client['test_db']
    test_collection = test_database['test_collection']
    DbWrapper.insert_many_to_collection([
        {'test1': [
            {'first_key': 'first_value'}, {'second_key': 'second_value'}
        ], 'test2': 'qwerty'
        },
        {'test3': 'somebody'},
        {'cool_test': {'wow': 'super'}}
    ], test_collection)
    return test_collection
