import pytest
from bs4 import BeautifulSoup
import enricher

with open('tests/detail-stub.html') as faux_wiki:
    page_fragment = faux_wiki.read()

soup = BeautifulSoup(page_fragment, 'html.parser')


def test_parse_population():
    infobox = soup.find('table', {'class': 'infobox'})
    museum_type = enricher.parse_population(infobox)

    assert museum_type == 2102650


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
