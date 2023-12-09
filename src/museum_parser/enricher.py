# from src.museum_parser.utils import fetcher
# from src.museum_parser.utils.museum import Museum

from museum_parser.utils import fetcher
from museum_parser.utils.museum import Museum
import re


def enrich_city_data(museum: Museum):
    print(f'enriching city data for {museum.name} ...')

    # infobox = fetcher.fetch_wiki_table(museum.city_wiki, {'class': 'infobox'})

    infobox = fetcher.fetch_wiki_page(wiki_page_name=museum.city_wiki).find('table', {'class': 'infobox'})

    # Parse population data
    museum.city_population = parse_population(infobox)
    museum.urban_population = parse_urban_population(infobox)

    return museum

def parse_population(infobox):
    # Parse general population data - prioritize layout with population and header inline ahead of pupoluation in subsequent row
    for label in infobox.find_all('th', {'class': ['infobox-label', 'infobox-header']}):
        if 'Population' in label.text:

            population = extract_population_figure(label.parent)

            if population is None:
                population = extract_population_figure(label.parent.findNext('tr'))

            break

    return population


def parse_urban_population(infobox):
    labels = infobox.find_all('a', {'title': 'Urban area'})

    if len(labels) == 0:
        return None

    # Either it's the first thing returned ... or we don't have it.
    population = extract_population_figure(labels[0].parent.parent)

    return population


def extract_population_figure(page_fragment):
    cell = page_fragment.find('td', {'class': 'infobox-data'})

    if cell is None:
        return None

    parsed_population = cell.text.replace(',', '').strip()
    try:
        parsed_population = int(re.match('([\d]*)', parsed_population).groups()[0])
    except:
        return None  # Cast failed - return None and deal with it upstream

    return parsed_population


def enrich_museum_details(museum: Museum):
    if museum.wiki is None:
        return

    print(f'enriching museum data for {museum.name} ...')

    wiki_page = fetcher.fetch_wiki_page(wiki_page_name=museum.wiki)
    infobox = wiki_page.find('table', {'class': 'infobox'})

    # infobox = fetcher.fetch_wiki_table(museum.wiki, {'class': 'infobox'})

    if infobox is None:
        return

    coords = parse_coordinates(wiki_page)
    if coords is not None:
        museum.longitude = coords["longitude"]
        museum.latitude = coords["latitude"]

    museum_type = parse_museum_type(infobox)
    museum.museum_type = museum_type

    return museum

def parse_coordinates(page_fragmetn):
    obj_coords = {"longitude": None, "latitude": None}

    geos = page_fragmetn.find('span', {'class': ['geo', 'deo-dms']})

    if geos is None:
        return None

    parsed_ccordinates = [coord.strip() for coord in geos.text.split('/')[-1].split(';')]

    if len(parsed_ccordinates) == 2:
        obj_coords["longitude"] = float(parsed_ccordinates[0])
        obj_coords["latitude"] = float(parsed_ccordinates[1])
    else:
        return None

    return obj_coords

def parse_museum_type(infobox):
    museum_type = None
    labels = infobox.find_all('th', {'class': 'infobox-label'})

    for label in labels:
        if label.text == 'Type':
            cell = label.parent.find('td', {'class': 'infobox-data'})
            museum_type = cell.text
            break

    return museum_type
