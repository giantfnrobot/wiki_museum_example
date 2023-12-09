from dataclasses import dataclass

@dataclass
class Museum:
    name: str = None
    wiki: str = None
    city: str = None
    city_wiki: str = None
    country: str = None
    country_wiki: str = None
    visitors: int = None
    city_population: int = None
    urban_population: int = None
    longitude: float = None
    latitude: float = None
    museum_type: str = None