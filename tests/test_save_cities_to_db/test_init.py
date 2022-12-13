import pytest

from project.save_cities_to_db import CitiesSaverToDb


class TestInit:

    def test_correct_work(self):
        obj = CitiesSaverToDb()
        assert obj.countries
        assert obj.cities




