import datetime
import pandas as pd
import sys

sys.path.append('src')

from src.museum_parser import parser


if __name__ == "__main__":

    if len(sys.argv) > 1:
        
        try:
            visitors = int(sys.argv[1])
        except:
            print(f'Invalid minimum visitors value: "{sys.argv[1]}". Must be an integer.')
            sys.exit()

        print(f'Filtering dataset to {visitors}')
        museum_df = parser.fetch_museum_data(minimum_visitors=visitors)
            
    else:
        museum_df = parser.fetch_museum_data() 
    
    filename = f'museum_data_{str(datetime.datetime.now().timestamp()).replace(".","")}.csv'

    print(f'writing data to: {filename}')
    museum_df.to_csv(f'workspace/data/{filename}', sep='\t', encoding='utf-8', index=False)