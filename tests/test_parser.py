import pytest
from bs4 import BeautifulSoup
from museum_parser import enricher
from museum_parser.utils.museum import Museum


with open('tests/detail-stub.html') as faux_wiki:
    page_fragment = faux_wiki.read()

soup = BeautifulSoup(page_fragment, 'html.parser')

museum_stub = {
        'museum_name': 'Museum Name',
        'museum_wiki_name': 'Wiki Name',
        'city_name': 'City Name',
        'city_wiki_name': 'City Wiki',
        'country_name': 'Country Name',
        'country_wiki_name': 'Country Wiki',
        'visitor_count': 0,
        'city_population': 1,
        'urban_population': 2,
        'longitude': 1.12345,
        'latitude': 1.67891,
        'museum_type': 'Museum Type'
    }


def test_parse_population():
    infobox = soup.find('table', {'class': 'infobox'})
    museum_type = enricher.parse_population(infobox)

    assert museum_type == 2102650


def test_parse_urban_population():
    infobox = soup.find('table', {'class': 'infobox'})
    museum_type = enricher.parse_urban_population(infobox)

    assert museum_type == 10858852


def test_parse_coordinates():
    parsed_ccordinates = enricher.parse_coordinates(soup)

    assert len(parsed_ccordinates) == 2


def test_parse_type():
    infobox = soup.find('table', {'class': 'infobox'})
    parsed_ccordinates = enricher.parse_museum_type(infobox)

    assert parsed_ccordinates == 'Art museum'


def test_ini(request):
    rootdir = request.config.rootdir
    assert (rootdir / 'pyproject.toml').isfile()


def test_museum_init():

    test_museum = Museum(
        name=museum_stub['museum_name'],
        wiki=museum_stub['museum_wiki_name'],
        city=museum_stub['city_name'],
        city_wiki=museum_stub['city_wiki_name'],
        country=museum_stub['country_name'],
        country_wiki=museum_stub['country_wiki_name'],
        visitors=museum_stub['visitor_count'],
        city_population=museum_stub['city_population'],
        urban_population=museum_stub['urban_population'],
        longitude=museum_stub['longitude'],
        latitude=museum_stub['latitude'],
        museum_type=museum_stub['museum_type']
    )

    assert type(test_museum) is Museum