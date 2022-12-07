from pathlib import Path
from bs4 import BeautifulSoup

import requests


class CitiesFetcher:

    URL_TO_CITIES_TABLE = 'https://www.macrotrends.net/cities/largest-cities-by-population'

    def __init__(self):
        if Path('cities.html').exists():
            self._parse_file()
        else:
            self.__create_file('cities.html')

    @staticmethod
    def _parse_file():
        dict_cities = {}
        counter = 0
        with open('cities.html') as cities:
            soup = BeautifulSoup(cities, 'lxml')
        for i in soup.find_all('tr'):
            dict_cities[int(i.find('td').get_text())] = [i.find('a').get_text(),
                                                         i.find('td',
                                                                style='text-align:left;').get_text(),
                                                         i.find('td',
                                                                style='text-align:right;').get_text()
                                                         ]
            counter += 1
            if counter == 50:
                break
        return dict_cities

    def __create_file(self, filename: str):
        try:
            request = requests.get(self.URL_TO_CITIES_TABLE)
        except Exception:
            raise ConnectionError("Помилка запиту. Ймовірно,у вас проблеми із інтернетом,"
                                  "перевірте з'єднання та спробуйте ще раз ")
        request_text = request.text
        soup = BeautifulSoup(request_text, 'lxml')
        table = soup.find('table', id='world_cities')
        table_body = table.find('tbody')
        with open(filename, 'w') as file:
            file.write(str(table_body))
        self._parse_file()


a = CitiesFetcher()
