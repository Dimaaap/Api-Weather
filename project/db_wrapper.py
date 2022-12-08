class DbWrapper:

    @staticmethod
    def insert_one_to_collection(data, collection: callable):
        try:
            collection.insert_one(data)
        except Exception as e:
            print(e)
            raise ConnectionError('Connection hes been lost')
        else:
            print('Data was inserted successfully')

    @staticmethod
    def insert_many_to_collection(data: list | tuple, collection: callable):
        try:
            collection.insert_many(data)
        except Exception as e:
            print(e)
            raise ConnectionError('Connection has been lost')

    @staticmethod
    def find_all_data_from_collection(collection: callable, filter_fields: dict,
                                      including_field: dict):
        try:
            result = collection.find(filter_fields, including_field)
        except Exception as e:
            print(e)
            raise ConnectionError('Connection has been lost')
        else:
            return result

    @staticmethod
    def find_one_from_collection(collection: callable, filter_fields: dict, including_fields: dict):
        try:
            result = collection.find_one(filter_fields, including_fields)
        except Exception as e:
            print(e)
            raise ConnectionError('Connection has been lost')
        else:
            return result

    def delete_many_from_collection(self, collection: callable, filter_fields: dict):
        try:
            deleting_list = self.find_all_data_from_collection(collection, filter_fields,
                                                               {'_id': 1}).limit(50)
            collection.delete_many({'_id': {'$in': list(deleting_list)}})
        except Exception as e:
            print(e)
            raise ConnectionError('connection has been lost')

    @staticmethod
    def count_number_documents_in_collection(collection, filter_fields):
        try:
            count = collection.count_documents(filter_fields)
        except Exception as e:
            print(e)
            raise ConnectionError('Connection has been lost')
        else:
            return count
