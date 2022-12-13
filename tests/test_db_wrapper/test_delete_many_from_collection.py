# import pytest
#
# from project.db_wrapper import DbWrapper
#
#
# class TestDbWrapper:
#
#     def test_correct_work(self, inserted_collection):
#         count_documents = DbWrapper.count_number_documents_in_collection(inserted_collection,
#                                                                          {'city': 'Kyiv'})
#         DbWrapper().delete_many_from_collection(inserted_collection, {'city': 'Kyiv'})
#         assert count_documents - 1 == inserted_collection.count_documents({})
