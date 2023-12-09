import datetime
import pandas as pd
import sys

sys.path.append('src/museum_parser')

from src.museum_parser import parser


if __name__ == "__main__":
    
    museum_df = parser.fetch_museum_data(minimum_visitors=2000000)
    filename = f'museum_data_{str(datetime.datetime.now().timestamp()).replace(".","")}.csv'

    print(f'writing data to: {filename}')
    museum_df.to_csv(f'workspace/data/{filename}', sep='\t', encoding='utf-8', index=False)