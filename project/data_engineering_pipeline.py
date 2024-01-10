import os
import sqlite3
import pandas as pd
""" Only for fetching data, also accepts license of Kaggle data use."""
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
from sklearn.model_selection import train_test_split


def download_dataset(competition_name, dataset_dir):
    print(f"Task 1(started): Data Downloading {competition_name}")
    api = KaggleApi()
    api.authenticate()
    api.competition_download_files(
        competition_name, path=dataset_dir, quiet=False)
    print("Task 1(Finished): Data Downloading")


"""Kaggle api returns data in zip form, need to be unzipped."""


def extract_zip(zip_path, output_directory):
    print(f"Task 2(started): Extraction for unzipping {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_directory)
    print("Task 2(Finished): Extraction for unzipping ")


def process_csv_files(dataset_dir, db_path):
    """We only need these 2 files. train has Asset id, which can help is get
        the name of cryptoasset and the weight each cryptoasset receives in
        the metric from asset_details file."""
    asset_details_path = os.path.join(dataset_dir, 'asset_details.csv')
    train_data_path = os.path.join(dataset_dir, 'train.csv')
    int_columns = ['timestamp', 'Asset_ID']
    float_columns = ['Count', 'Open', 'High', 'Low', 'Close',
                     'Volume', 'VWAP', 'Target', 'Weight']

    if os.path.exists(asset_details_path) and os.path.exists(train_data_path):
        print("Task 3(started): Processing the csv files")
        chunk_size = 10000
        asset_details_chunk = pd.read_csv(asset_details_path,
                                          chunksize=chunk_size)
        train_data_chunk = pd.read_csv(train_data_path,
                                       chunksize=chunk_size)
        combined_chunks = []
        for asset_chunk, train_chunk in zip(asset_details_chunk,
                                            train_data_chunk):
            combined_chunk = pd.merge(train_chunk, asset_chunk,
                                      on='Asset_ID')
            """VWAP has 9 nan values, this will fix the database"""
            combined_chunk = combined_chunk.dropna()
            combined_chunks.append(combined_chunk)
        combined_data = pd.concat(combined_chunks)
        print("Task 3(Finished): Processing the CSV files")
        print("Task 4(started): dtype mapping for memory optimization")
        dtype_map = {col: 'int32' for col in int_columns}
        dtype_map.update({col: 'float32' for col in float_columns})

        combined_data = combined_data.astype(dtype_map)
        print("Task 4(Finished): Applying dtype mapping")

        train, val_test = train_test_split(combined_data, test_size=0.3,
                                           random_state=42)
        val, test = train_test_split(val_test, test_size=0.5,
                                     random_state=42)
        with sqlite3.connect(db_path) as conn:
            train.to_sql('train_data', conn,
                         if_exists='replace', index=False)
            val.to_sql('validation_data', conn,
                       if_exists='replace', index=False)
            test.to_sql('test_data', conn,
                        if_exists='replace', index=False)
        conn.close()
        print("Saved splitted data to sql database.")
    else:
        print(f"Files not found: {asset_details_path} or {train_data_path}")


def main():
    competition_name = 'g-research-crypto-forecasting'
    dataset_dir = ('data/')  
    db_path = os.path.join(dataset_dir, 'data.db')

    print("Task 0: Setting up the directories for everything")
    os.makedirs(dataset_dir, exist_ok=True)
    download_dataset(competition_name, dataset_dir)

    zip_file_path = os.path.join(dataset_dir, competition_name + '.zip')
    if os.path.exists(zip_file_path):
        extract_zip(zip_file_path, dataset_dir)
        os.remove(zip_file_path)

    process_csv_files(dataset_dir, db_path)

    print("Data pipeline is finished without any problem.")


if __name__ == "__main__":
    main()
