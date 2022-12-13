from pathlib import Path

from project.fetch_cities import CitiesFetcher


class TestCreateFile:

    def test_creating(self, temp_file):
        obj = CitiesFetcher()
        obj._CitiesFetcher__create_file(temp_file)
        assert Path('cities.html').exists()

    def test_exists_attribute(self, url_to_cities_table):
        obj = CitiesFetcher()
        assert obj.URL_TO_CITIES_TABLE
        assert obj.URL_TO_CITIES_TABLE == url_to_cities_table
