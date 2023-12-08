from utils.fetcher import Fetcher 
from utils.museum import Museum
import re

class Enricher:

    def __init__(self, museum):
        self.enriched_museum: Museum = museum


    def enrich_city_data(self):
        print(f'fetchhing city poplulation data for {self.enriched_museum.name} ...')

        f = Fetcher()

        infobox = f.fetch_wiki_table(self.enriched_museum.city_wiki, {'class': 'infobox'})

        # Parse general population data - prioritize layout with population and header inline ahead of pupoluation in subsequent row
        for label in infobox.find_all('th', {'class': ['infobox-label', 'infobox-header']}):
            if 'Population' in label.text:
                
                population = self._extract_population_figure(label.parent)
                    
                if population is None:
                    population = self._extract_population_figure(label.parent.findNext('tr'))

                self.enriched_museum.city_population = population 

                break
        
        # Parse urban population data
        self._parse_urban_population(infobox)


    def _parse_urban_population(self, infobox):
        
        labels = infobox.find_all('a', {'title': 'Urban area'})

        if len(labels) == 0:
            return None

        # Either it's the first thing returned ... or we don't have it.
        population = self._extract_population_figure(labels[0].parent.parent)
        self.enriched_museum.urban_population = population  


    def _extract_population_figure(self, page_fragment):

        cell = page_fragment.find('td', {'class': 'infobox-data'})

        if cell is None:
            return None
        
        parsed_population = cell.text.replace(',','').strip()
        try:
            parsed_population = int(re.match('([\d]*)', parsed_population).groups()[0])
        except:
            return None # Cast failed - return None and deal with it upstream
        
        return parsed_population
    

    def enrich_museum_details(self):
        
        if self.enriched_museum.wiki is None:
            return 
        
        print(f'fetchhing museum details for {self.enriched_museum.name} ...')

        f = Fetcher()

        museum_table = f.fetch_wiki_table(self.enriched_museum.wiki, {'class': 'infobox'})

        if museum_table is None:
            return 

        labels = museum_table.find_all('th', {'class': 'infobox-label'})
        
        # Parse Coordinates and Type
        for label in labels:
            if label.text in ['Coordinates', 'Type']:
                cell = label.parent.find('td', {'class': 'infobox-data'})
                match label.text:
                    case 'Coordinates':
                        parsed_ccordinates = [coord.strip() for coord in cell.text.split('/')[-1].split(';')]
                        if  parsed_ccordinates[0] is not None: self.enriched_museum.longitude = float(parsed_ccordinates[0])
                        if  parsed_ccordinates[1] is not None: self.enriched_museum.latitude = float(parsed_ccordinates[1])
                    case 'Type':
                        self.enriched_museum.museum_type = cell.text