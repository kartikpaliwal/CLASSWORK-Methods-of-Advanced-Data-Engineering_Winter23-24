"""
TASKS: 
# Build an automated data pipeline for the following source:
    *direct link to CSV: https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV

# Goals: 
1. Write data into a SQLite database called “trainstops.sqlite”, in the table “trainstops”
2. First, drop the "Status" column
3. Then, drop all rows with invalid values:
   3.1 Valid "Verkehr" values are "FV", "RV", "nur DPN"
   3.2 Valid "Laenge", "Breite" values are geographic coordinate system values between and including -90 and 90
   3.3 Valid "IFOPT" values follow this pattern:
       *  <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
       *  This is not the official IFOPT standard, please follow our guidelines and not the official standard
   3.4Empty cells are considered invalid
4. Use fitting SQLite types (e.g., BIGINT, TEXT or FLOAT) for all columns

"""


import pandas as pd
import sqlalchemy as sql

class Data_Fetcher:
    def __init__(self, url, db_name, table_name):
        self.df = None
        self.url = url
        self.db_name = db_name
        self.table_name = table_name

    def reader(self):
        self.df = pd.read_csv(self.url, delimiter=';') \
                    .drop(columns='Status', errors='ignore') 
        
        if self.df is not None:
            self.df.dropna(subset=self.df.columns.to_list(), inplace=True) 
            self.df = self.df.loc[self.df['IFOPT'].str.match(r'^.{2}:\d+:\d+(?::\d+)?$').fillna(False)]

            self.df['Laenge'] = pd.to_numeric(self.df['Laenge'].str.replace(',', '.'), errors='coerce')
            self.df['Breite'] = pd.to_numeric(self.df['Breite'].str.replace(',', '.'), errors='coerce')

            self.df = self.df[self.df['Laenge'].between(-90, 90) & self.df['Breite'].between(-90, 90)]
            

            Database_Connection = sql.create_engine(f"sqlite:///{self.db_name}.sqlite", echo=False)

            datatype_convertor = {
                'NAME': sql.types.TEXT,
                'Verkehr': sql.types.TEXT,
                'IFOPT': sql.types.TEXT,
                'Laenge': sql.types.FLOAT,
                'Breite': sql.types.FLOAT,
                'DS100': sql.types.TEXT,
                'Betreiber_Name': sql.types.TEXT,
                'Betreiber_Nr': sql.types.BIGINT,
                'EVA_NR': sql.types.BIGINT,
            }

            self.df.to_sql(self.table_name, con=Database_Connection, if_exists="replace", index=False, dtype=datatype_convertor)
        return self.df.copy()

if __name__ == '__main__':
    db_url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
    db_name = 'trainstops'
    table_name = 'trainstops'

    Fetch_data = Data_Fetcher(db_url, db_name, table_name)
    df = Fetch_data.reader()