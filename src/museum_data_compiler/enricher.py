from utils.fetcher import Fetcher as f
from utils.museum import Museum
import re

class Enricher:

    def __init__(self, museum):
        self.enriched_museum: Museum = museum

    def enrich_city_data(self):
        print('fetchhing city poplulation data ...')

        city_table = f.fetch_wiki_table(self.enriched_museum.city_wiki, {"class": "infobox"})

        # Parse urban population data
        labels = city_table.find_all('a', {'title': 'Urban area'})

        if len(labels) > 0:
            for label in labels:
                population = self._parse_population_figure(label.parent.parent)
                self.enriched_museum.urban_population = population

        # Parse general population data - prioritize layout with population and header inline ahead of pupoluation in subsequent row
        for label in city_table.find_all('th', {'class': ['infobox-label', 'infobox-header']}):
            if 'Population' in label.text:
                
                population = self._parse_population_figure(label.parent)
                    
                if population is None:
                    population = self._parse_population_figure(label.parent.findNext('tr'))

                self.enriched_museum.city_population = population 

                break

    def _parse_population_figure(self, page_fragment):

        cell = page_fragment.find('td', {"class": "infobox-data"})

        if cell is not None:
            parsed_population = cell.text.replace(',','').strip()
            try:
                parsed_population = int(re.match('([\d]*)', parsed_population).groups()[0])
            except:
                return None # Cast failed - return None and deal with it upstream
            
            return parsed_population
        
        return None
    
    def enrich_museum_details(self):
        print('fetchhing museum details ...')

        if self.enriched_museum.wiki is None:
            return 

        museum_table = f.fetch_wiki_table(self.enriched_museum.wiki, {"class": "infobox"})

        if museum_table is None:
            return 

        labels = museum_table.find_all('th', {'class': 'infobox-label'})
        
        for label in labels:
            if label.text in ['Coordinates', 'Type']:
                cell = label.parent.find('td', {"class": "infobox-data"})
                match label.text:
                    case 'Coordinates':
                        parsed_ccordinates = [coord.strip() for coord in cell.text.split('/')[-1].split(';')]
                        self.enriched_museum.longitude = parsed_ccordinates[0]
                        self.enriched_museum.latitude = parsed_ccordinates[1]
                    case 'Type':
                        self.enriched_museum.museum_type = cell.text