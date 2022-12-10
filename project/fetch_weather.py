import requests
from os import getenv
import json
from typing import List
import datetime

from progressbar import ProgressBar

from mixins import ConnectToMongoMixin
from db_wrapper import DbWrapper


class FetchWeather(ConnectToMongoMixin, DbWrapper):
    API_TOKEN = getenv('API_TOKEN')
    MAX_DOCUMENTS_COUNT = 400

    def __init__(self):
        super().__init__()
        self.cities = self.database['cities']
        self.weather = self.database['weather']

    @staticmethod
    def form_request_url(city: str, token: str = API_TOKEN):
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'
        return weather_url

    def fetch_weather_to_cities(self):
        list_weather = []
        count = 0
        print('Start fetching weather for cities')

        with ProgressBar(max_value=50) as bar:
            for city in self.cities.find({}, {'city_title': 1, '_id': 0}):
                city_title = city['city_title']
                try:
                    weather_city_data = requests.get(self.form_request_url(city_title))
                except Exception:
                    raise ConnectionError('Connection has been lost')
                json_weather_city_data = json.loads(weather_city_data.text)
                list_weather.append(json_weather_city_data)
                count += 1
                bar.update(count)

        self.__parse_weather_data(list_weather)

    def __parse_weather_data(self, weather_data: list):
        weather_list = []
        weather_data = self.__change_temperature_dict_to_celsius(weather_data)
        for i in range(len(weather_data)):
            weather_list.append({'city_id': i + 1, 'weather_data': weather_data[i],
                                 'time_insert': datetime.datetime.now()})
        self.insert_many_to_collection(weather_list, self.weather)

    def update_weather_data(self):
        pass

    def __change_temperature_dict_to_celsius(self, weather_data):
        keys_list = list(weather_data[0]['main'].keys())[:4]
        for i in range(len(weather_data)):
            degrees_list = list(weather_data[i]['main'].values())[:4]
            change_degree_list = self.__convert_list_temperature(degrees_list)
            for index, element in enumerate(keys_list):
                weather_data[i]['main'][element] = change_degree_list[index]
        return weather_data

    @staticmethod
    def __convert_list_temperature(list_temperature: List[int | float]) -> List[int | float]:
        convert_list = list(map(lambda temperature: round(temperature - 272.15, 2),
                                list_temperature))
        return convert_list

    def start(self):
        self.fetch_weather_to_cities()
        self.clear_collection(self.weather, self.MAX_DOCUMENTS_COUNT)


a = FetchWeather()
a.start()
