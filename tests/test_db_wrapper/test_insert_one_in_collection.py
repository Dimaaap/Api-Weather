import pytest

from project.db_wrapper import DbWrapper

cases_for_insert_one = [
    ({'test1': 'test1'}, 1),
    ({}, 1),
    ({'test_case1': [{
        'test_number': 3
    }, {
        'test_number': 4
    }]}, 1),
    ({'Hello': 'Hello'}, 1)
]


class TestInsertOneToCollection:

    @pytest.mark.parametrize('data, count', cases_for_insert_one)
    def test_insert_one_to_collection(self, connect_to_db, data, count):
        DbWrapper.insert_one_to_collection(data, connect_to_db)
        assert connect_to_db.count_documents({}) == count

    @pytest.mark.parametrize('data, value', [
        (1, 1),
        (3, 'will be failed'),
        (2, 'also will be failed')
    ])
    def test_catch_errors(self, connect_to_db, data, value):
        with pytest.raises(ConnectionError):
            DbWrapper.insert_one_to_collection({data: value}, connect_to_db)
