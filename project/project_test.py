import os
import pandas as pd
from data_engineering_pipeline import (download_dataset,
                                       extract_zip,
                                       process_csv_files)


def test_download_dataset(dataset_dir, competition_name):
    download_dataset(competition_name, dataset_dir)
    zip_file_exists = os.path.exists(
        os.path.join(dataset_dir, competition_name + '.zip'))
    assert zip_file_exists, "Download failed: Zip file not found"
    print("Download Dataset: Test Passed")


def test_extract_zip(zip_file_path, output_directory):
    extract_zip(zip_file_path, output_directory)
    expected_file = 'train.csv'
    file_exists = os.path.exists(os.path.join(output_directory, expected_file))
    assert file_exists, "Extraction failed: Expected file not found"
    print("Extract Zip: Test Passed")


def test_process_csv_files(dataset_dir, db_path):
    process_csv_files(dataset_dir, db_path)
    print("Process CSV Files: Test Passed")


def test_integrity(csv_file_path):
    assert os.path.exists(csv_file_path), (
        f"CSV file {csv_file_path} does not exist")
    df = pd.read_csv(csv_file_path)
    assert len(df) > 0, "Data Integrity Failed: CSV file is empty"
    assert os.path.exists(csv_file_path), (
        f"CSV file {csv_file_path} does not exist")

    print("Data Integrity of the CSV file: Test Passed")


def run_tests():
    competition_name = 'g-research-crypto-forecasting'
    dataset_dir = os.path.join('/home/kryp/Documents/uni work/Advanced data engineering/github assignments/CLASSWORK-Methods-of-Advanced-Data-Engineering_Winter23-24/', 'data/')  # noqa
    db_path = os.path.join(dataset_dir, 'data.db')
    csv_file_path = os.path.join(dataset_dir, 'train.csv')

    test_download_dataset(dataset_dir, competition_name)
    test_extract_zip(
        os.path.join(dataset_dir, competition_name + '.zip'), dataset_dir)
    test_process_csv_files(dataset_dir, db_path)
    test_integrity(csv_file_path)


if __name__ == "__main__":
    run_tests()
