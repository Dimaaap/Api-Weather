from fetch_cities import CitiesFetcher
from mixins import ConnectToMongoMixin
from db_wrapper import DbWrapper


class CitiesSaverToDb(CitiesFetcher, ConnectToMongoMixin, DbWrapper):

    def __init__(self):
        ConnectToMongoMixin.__init__(self)
        self.cities = self.database['cities']
        self.countries = self.database['countries']
        self.dict_cities = super()._parse_file()

    def __insert_countries(self):
        countries_set = set()
        for i in self.dict_cities.values():
            countries_set.add(i[1])
        try:
            for index, country in enumerate(countries_set):
                if not self.find_one_from_collection(self.cities, {'country_title': country}, {}):
                    self.insert_one_to_collection({'id': index + 1, 'country_title': country},
                                                  self.countries)
                else:
                    continue
        except Exception:
            raise ConnectionError('Connection has been lost')

    def __insert_cities(self):
        cities_list = []
        for i in self.dict_cities:
            cities_list.append((i, *self.dict_cities[i]))
        try:
            for city_id, city_title, country, population in cities_list:
                population = self.convert_population_by_int(population)
                country_id = self.find_one_from_collection(self.countries,
                                                           {'country_title': country},
                                                           {'id': 1, '_id': 0})
                if not self.find_one_from_collection(self.cities, {'city_title': city_title}, {}):
                    self.insert_one_to_collection({'id': city_id, 'city_title': city_title,
                                                   'country_id': country_id['id'],
                                                   'population': population}, {})
                else:
                    continue
        except Exception:
            raise ConnectionError('An error occurred when connecting to the database.'
                                  ' Check your connection and try again')

    @staticmethod
    def convert_population_by_int(population: str):
        return int(population.replace(',', ''))

    def start(self):
        self.__insert_countries()
        self.__insert_cities()


a = CitiesSaverToDb()
a.start()
