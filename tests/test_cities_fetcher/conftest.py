from pathlib import Path

import pytest


@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / 'cities.html'
    file.write_text('Hello')
    yield file
    Path(file).unlink()


@pytest.fixture
def url_to_cities_table_with_deleted_file():
    yield 'https://www.macrotrends.net/cities/largest-cities-by-population'
    Path('cities.html').unlink()


@pytest.fixture
def url_to_cities_table():
    return 'https://www.macrotrends.net/cities/largest-cities-by-population'

