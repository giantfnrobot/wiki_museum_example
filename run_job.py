import datetime
import pandas as pd
from museum_data_compiler import MuseumParser


if __name__ == "__main__":
    
    m = MuseumParser()
    museum_df = m.fetch_museum_data()
    filename = f'museum_data_{datetime.datetime.now().microsecond}.csv'

    print(f'writing data to: {filename}')
    museum_df.to_csv(f'/data/{filename}', sep='\t', encoding='utf-8')