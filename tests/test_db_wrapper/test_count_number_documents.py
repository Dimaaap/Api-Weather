import pytest

from project.db_wrapper import DbWrapper

case_to_test_work = [
    ({}, 6),
    ({'city': 'Kyiv'}, 1),
    ({'city': {'$in': ['Ternopil', 'Kharkiv']}}, 2),
    ({'city': 'London'}, 0)
]

case_to_test_assertion = [
    {1: 12},
    {4: '4'}
]


class TestCountNumber:

    def test_correct_work_simple(self, inserted_collection):
        count_docs = inserted_collection.count_documents({})
        count_docs_wrapper = DbWrapper.count_number_documents_in_collection(inserted_collection,
                                                                            {})
        assert count_docs == count_docs_wrapper

    @pytest.mark.parametrize('filter_fields, count', case_to_test_work)
    def test_correct_work_parametrize(self, inserted_collection, filter_fields, count):
        count_docs_wrapper = DbWrapper.count_number_documents_in_collection(inserted_collection,
                                                                            filter_fields)
        assert count_docs_wrapper == count

    @pytest.mark.parametrize('filter_fields', case_to_test_assertion)
    def test_assertion(self, inserted_collection, filter_fields):
        with pytest.raises(ConnectionError):
            DbWrapper.count_number_documents_in_collection(inserted_collection, {1: 12})

    def test_connect_to_not_exists_collection(self):
        with pytest.raises(ConnectionError):
            exists_collection = ''
            DbWrapper.count_number_documents_in_collection(exists_collection, {})
