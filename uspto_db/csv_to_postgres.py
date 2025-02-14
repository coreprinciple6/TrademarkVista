import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def load_data_to_postgres():
    # Create SQLAlchemy engine
    engine = create_engine('postgresql://localhost/trademark_db')
    
    # Read CSV file
    df = pd.read_csv('data/csv_files/trademarks_100.csv')
    
    # Rename columns to match PostgreSQL schema
    df.columns = [
        'category_code',
        'mark_identification',
        'serial_number',
        'case_file_owners',
        'status',
        'xml_filename'
    ]
    
    # Clean data
    df = df.replace({np.nan: None})
    
    # Load to PostgreSQL
    df.to_sql('trademarks', 
              engine, 
              if_exists='append',
              index=False,
              method='multi',
              chunksize=1000)

if __name__ == "__main__":
    try:
        load_data_to_postgres()
        print("Data import successful")
    except Exception as e:
        print(f"Error: {e}")