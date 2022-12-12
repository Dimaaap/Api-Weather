import pytest

from project.db_wrapper import DbWrapper

cases_insert_many = [
    {
        'weather': {'temperature': 'test',
                    'pressure': 'also_test'},
        'city_title': 'city_test'
    },
    {
        'weather': {'temperature': 'test1',
                    'pressure': 'also_test1'},
        'city_title': 'test_city'
    },
    {
        'weather': {'temperature': 'test2'},
        'city_title': 'test_city2'
    }]

cases_to_raise_value = [
    (1, 'This error'),
    (2, 'Also error')
]

cases_to_insert_one = [
    ({'test_insert_one1': 'value1'}),
    ({'test_insert_one2': 2}),
    ({(1, 2, 3): 3})
]


class TestInsertMany:

    def test_insert_many(self, connect_to_db):
        DbWrapper.insert_many_to_collection(cases_insert_many, collection=connect_to_db)
        assert connect_to_db.count_documents({}) == 3

    @pytest.mark.parametrize('data, value', cases_to_raise_value)
    def test_raise_error(self, connect_to_db, data, value):
        with pytest.raises(ConnectionError):
            DbWrapper.insert_many_to_collection({data: value}, connect_to_db)

    @pytest.mark.parametrize('inserted_data', cases_to_insert_one)
    def test_work_with_insert_one(self, connect_to_db, inserted_data):
        with pytest.raises(ConnectionError):
            DbWrapper.insert_many_to_collection(inserted_data, connect_to_db)

