import pandas as pd
import urllib.parse

from utils.fetcher import Fetcher 
from utils.museum import Museum
from enricher import Enricher 

class MuseumParser:

    def __init__(self):
        self.city_record = {}
        self.museum_list = []

    def fetch_museum_data(self, minimum_visitors=0):
        print('fetchhing museum list ...')

        f = Fetcher()

        wiki_table_rows = f.fetch_wiki_table_rows(wiki_page_name='List_of_most-visited_museums', table_identifier={"class": "wikitable sortable"})

        # Iterate over table rows (i.e. museums) and parse data into a list of Museum objects
        for row in wiki_table_rows:
            
            museum_obj = self._parse_museum_row(row)

            """
            Dumping data seems like a poor idea if we want to build a basic regression.
            However, the framing of the problem suggests this should be the case.  Accordinly, the filter can be applied here.
            """
            if museum_obj.visitors < minimum_visitors: # Filter on minimum visitors.
                continue                                

            e = Enricher(museum_obj)

            print(f'enriching record for {museum_obj.name} ...')

            # Only fetch the city data if it has not already been parsed/cached.
            if museum_obj.city not in self.city_record: 
                e.enrich_city_data()
                self.city_record[museum_obj.city] = {
                    'city_population': e.enriched_museum.city_population, 
                    'urban_population': e.enriched_museum.urban_population
                    }
            else: 
                e.enriched_museum.city_population = self.city_record[museum_obj.city]['city_population']
                e.enriched_museum.urban_population = self.city_record[museum_obj.city]['urban_population']

            if museum_obj.wiki is not None:
                e.enrich_museum_details()

            self.museum_list.append(e.enriched_museum)

        # Return a Dataframe and strip out the columns irrelevant to downstream analysis jobs.
        return pd.DataFrame(self.museum_list).drop(['wiki', 'city_wiki', 'country_wiki'], axis=1, inplace=True)

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
        visitor_count = int(cells[2].contents[0].replace(',','').strip())

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
    museum_df = m.fetch_museum_data(minimum_visitors=2000000)
    print(museum_df)