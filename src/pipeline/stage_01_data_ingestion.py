import os
from zipfile import ZipFile
from src.utils.common import read_yaml
from src import logger
import urllib.request as request
from src.constants import *
from src.exception import CustomException
import argparse
import sys


class DataIngestion:
    """
    A class to handle data ingestion tasks such as downloading and extracting zip files.

    """

    def __init__(self, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(params_filepath)

    def download_file(self):
        try:
            if not os.path.exists(self.config.data_ingestion.zip_file_path):
                print("downloading data...")
                filename, headers = request.urlretrieve(url=self.config.data_ingestion.s3_source,
                                                        filename=self.config.data_ingestion.zip_file_path)
                logger.info(
                    f"{filename} download! with following info: \n{headers}")
            else:
                logger.info("File already exists")

        except Exception as e:
            raise CustomException(e, sys)

    def extract_zip_file(self):
        try:
            with ZipFile(self.config.data_ingestion.zip_file_path, "r") as zip:
                zip.extractall(self.config.data_ingestion.unzip_file_path)
                logger.info(f"File unzip and extracted")
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=Path("params.yaml"))
    parsed_args = args.parse_args()
    data_ingestion = DataIngestion(params_filepath=parsed_args.config)

    # data_ingestion = DataIngestion(params_filepath=PARAMS_FILE_PATH)
    data_ingestion.download_file()
    data_ingestion.extract_zip_file()
