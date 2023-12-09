import pandas as pd
import urllib.parse

# from src.museum_parser.utils import fetcher
# from src.museum_parser.utils.museum import Museum
# from src.museum_parser import  enricher 

import utils

from utils import fetcher
from utils.museum import Museum
import  enricher



# def __init__(self):
city_record = {}
museum_list = []

def fetch_museum_data(minimum_visitors=0):
    print('fetching museum list ...')

    # wiki_table_rows = fetcher.fetch_wiki_table_rows(wiki_page_name='List_of_most-visited_museums',
    #                                                 row_identifier={"class": "wikitable sortable"})

    wiki_table_rows = (fetcher.fetch_wiki_page(wiki_page_name='List_of_most-visited_museums')
                       .find('table', {'class': 'wikitable sortable'})
                       .find_all('tr')[1:])

    # Iterate over table rows (i.e. museums) and parse data into a list of Museum objects
    for row in wiki_table_rows:

        museum_obj = parse_museum_row(row)

        """
        Dumping data seems like a poor idea if we want to build a basic regression.
        However, the framing of the problem suggests this should be the case.  
        Accordinly, the filter can be applied here.
        """
        if museum_obj.visitors < minimum_visitors:  # Filter on minimum visitors.
            continue

            # Only fetch the city data if it has not already been parsed/cached.
        if museum_obj.city not in city_record:
            museum_obj = enricher.enrich_city_data(museum_obj)
            city_record[museum_obj.city] = {
                'city_population': museum_obj.city_population,
                'urban_population': museum_obj.urban_population
            }
        else:
            museum_obj.city_population = city_record[museum_obj.city]['city_population']
            museum_obj.urban_population = city_record[museum_obj.city]['urban_population']

        if museum_obj.wiki is not None:
            museum_obj = enricher.enrich_museum_details(museum_obj)

        museum_list.append(museum_obj)

    # Strip out the columns irrelevant to downstream analysis jobs and return a Dataframe 
    df_museums = pd.DataFrame(museum_list)
    df_museums.drop(['wiki', 'city_wiki', 'country_wiki'], axis=1, inplace=True)

    return df_museums

def parse_museum_row(row):
    cells = row.find_all('td')

    # Extract museum name and wiki page name
    museum_link = cells[0].find_all('a')[1]
    museum_name = museum_link.contents[0]
    museum_wiki_name = urllib.parse.unquote(museum_link["href"]).replace('/wiki/', '')

    print(f'... parsing record for {museum_name}')

    if 'redlink' in museum_wiki_name:  # Here's an unfortuante edge case we need to check
        museum_wiki_name = None

    # Extract city and country names and wiki page names
    location_link_list = cells[1].find_all('a')
    city_name = location_link_list[0].contents[0]
    city_wiki_name = urllib.parse.unquote(location_link_list[0]["href"]).replace('/wiki/', '')

    if len(location_link_list) > 1:
        country_name = location_link_list[1].contents[0]
        country_wiki_name = urllib.parse.unquote(location_link_list[1]["href"]).replace('/wiki/', '')
    else:
        # We're dealing with a city state or a formatting problem.
        split_city_name = city_name.split(',')
        if len(split_city_name) == 2:
            city_name = split_city_name[0].strip()
            country_name = split_city_name[1].strip()
            country_wiki_name = country_name  # This will work most of the time.
        else:
            country_name = city_name
            country_wiki_name = city_wiki_name

    # Extract visitor count
    visitor_count = int(cells[2].contents[0].replace(',', '').strip())

    return Museum(
        name=museum_name,
        wiki=museum_wiki_name,
        city=city_name,
        city_wiki=city_wiki_name,
        country=country_name,
        country_wiki=country_wiki_name,
        visitors=visitor_count
    )

if __name__ == "__main__":
    museum_df = fetch_museum_data(minimum_visitors=4000000)
    print(museum_df.to_string())