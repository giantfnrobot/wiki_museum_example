import pandas as pd
import urllib.parse
from bs4 import BeautifulSoup

from utils.fetcher import Fetcher as f
from utils.museum import Museum
from enricher import Enricher as e

class MuseumParser:

    def __init__(self):
        self.city_record = {}
        self.museum_list = []

    def fetch_museum_data(self):
        print('fetchhing museum list ...')

        museum_table = f.fetch_wiki_table('List_of_most-visited_museums', {"class": "wikitable sortable"})

        for row in museum_table.find_all('tr')[1:]:
            
            museum_obj = self._parse_museum_row(row)
            enricher = e(museum_obj)

            print(f'enriching record for {museum_obj.name} ...')

            if museum_obj.city not in self.city_record: 
                enricher.enrich_city_data()
                self.city_record[museum_obj.city] = {
                    'city_population': enricher.enriched_museum.city_population, 
                    'urban_population': enricher.enriched_museum.urban_population
                    }
            else: 
                enricher.enriched_museum.city_population = self.city_record[museum_obj.city]['city_population']
                enricher.enriched_museum.urban_population = self.city_record[museum_obj.city]['urban_population']

            if museum_obj.wiki is not None:
                enricher.enrich_museum_details()

            self.museum_list.append(enricher.enriched_museum)

        return pd.DataFrame(self.museum_list)

    def _parse_museum_row(self, row):

        cells = row.find_all('td')

        # Extract museum name and wiki page name
        museum_link = cells[0].find_all('a')[1]
        museum_name = museum_link.contents[0]
        museum_wiki_name = urllib.parse.unquote(museum_link["href"]).replace('/wiki/', '')

        if 'redlink' in museum_wiki_name:    # Here's an unfortuante edge case we need to check 
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
                country_wiki_name = country_name    # This will work most of the time. 
            else:
                country_name = city_name
                country_wiki_name = city_wiki_name
        
        # Extract visitor count
        visitor_count = cells[2].contents[0].replace(',','').strip()

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
    m = MuseumParser()
    museum_df = m.fetch_museum_data()
    print(museum_df)