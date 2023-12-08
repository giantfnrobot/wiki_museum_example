import datetime
import pandas as pd
from museum_data_compiler import MuseumParser


if __name__ == "__main__":
    
    m = MuseumParser()
    museum_df = m.fetch_museum_data(minimum_visitors=2000000)
    filename = f'museum_data_{str(datetime.datetime.now().timestamp()).replace(".","")}.csv'

    print(f'writing data to: {filename}')
    museum_df.to_csv(f'workspace/data/{filename}', sep='\t', encoding='utf-8', index=False)