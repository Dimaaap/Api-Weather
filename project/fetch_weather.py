import requests
from os import getenv
import json


import progressbar

from save_cities_to_db import ConnectToMongoMixin


class FetchWeather(ConnectToMongoMixin):
    API_TOKEN = getenv('API_TOKEN')

    def __init__(self):
        super().__init__()
        self.cities = self.database['cities']
        self.weather = self.database['weather']
        cursor = self.weather.find()
        if len(list(cursor)) == 0:
            self.fetch_weather_to_cities()
        else:
            self.update_weather_data()

    @staticmethod
    def form_request_url(city: str, token: str = API_TOKEN):
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'
        return weather_url

    def fetch_weather_to_cities(self):
        list_weather = []

        count = 0
        print('Start fetching weather for cities')
        with progressbar.ProgressBar(max_value=50) as bar:
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
        self.parse_weather_data(list_weather)

    def parse_weather_data(self, weather_data: list):
        weather_list = []
        for i in range(len(weather_data)):
            weather_list.append({'city_id': i + 1, 'weather_data': weather_data[i]})
        self.save_to_db_weather(weather_list)

    def save_to_db_weather(self, weather_list: list[dict]):
        try:
            self.weather.insert_many(weather_list)
        except Exception:
            raise ConnectionError('Failed inserted to db')
        else:
            print('Data inserted successfully')

    def update_weather_data(self):
        pass


a = FetchWeather()
