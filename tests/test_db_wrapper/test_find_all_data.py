import pytest

from project.db_wrapper import DbWrapper

cases_to_find_data = [
    (
        {'test3': 'somebody'}
    ),
    (
        {'cool_test': {'wow': 'somebody'}}
    )
]


class TestFindAll:

    @pytest.mark.parametrize('data_to_find', cases_to_find_data)
    def test_correct_work(self, insert_data_to_database, data_to_find):
        result = DbWrapper.find_all_data_from_collection(collection=
                                                         insert_data_to_database,
                                                         filter_fields=
                                                         data_to_find,
                                                         including_field={})
        assert list(result) == list(insert_data_to_database.find(data_to_find))
