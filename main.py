# API KEY = d7c7f07afc41182d46b520579b622a3c






import requests
from os import getenv
from pprint import pprint

API_KEY = getenv('API_KEY')

api_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={"Madrid"}&appid={API_KEY}'
data = requests.get(api_weather_url)
pprint(data.text)
