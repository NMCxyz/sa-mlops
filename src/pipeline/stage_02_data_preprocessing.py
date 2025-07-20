from src.utils.common import read_yaml
from src import logger
from src.constants import *
from src.exception import CustomException
import argparse
import sys

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split


class Data_Preprocessing:
    def __init__(self, params_file=PARAMS_FILE_PATH):
        self.config = read_yaml(params_file)

    def display_dataset(self):
        df = pd.read_csv(self.config.data_load.dataset_path)
        print(f"\n{df.head()}")

    def handle_outliers(self, df):
        try:
            # self.Boundary_GD(df.avg_glucose_level, "avg_glucose_level")
            # self.Boundary_GD(df.bmi, 'bmi')

            df.loc[df['avg_glucose_level'] <= 63.3, 'avg_glucose_level'] = 63.3
            df.loc[df['avg_glucose_level'] >= 175, 'avg_glucose_level'] = 175

            df.loc[df['bmi'] <= 22.5, 'bmi'] = 22.5
            df.loc[df['bmi'] >= 36.5, 'bmi'] = 36.5

        except Exception as e:
            raise CustomException(e, sys)

    def Boundary_GD(self, feature, name):
        try:
            '''
            We use below method if follow a Gaussian Distribution

            '''

            # uppper_boundary=feature.mean() + 3* feature.std()
            # lower_boundary=feature.mean() - 3* feature.std()

            uppper_boundary = feature.mean() + feature.std()
            lower_boundary = feature.mean() - feature.std()
            print(name), print(lower_boundary), print(
                uppper_boundary), print(feature.mean())
            print(10*'-')
        except Exception as e:
            raise CustomException(e, sys)

    def split_save_train_test(self, df):
        try:
            logger.info('split the dataset section...')
            train_path = self.config.split_data.train_path
            test_path = self.config.split_data.test_path
            split_size = self.config.split_data.test_size

            train, test = train_test_split(df, test_size=split_size)

            train.to_csv(train_path, sep=",", index=False, encoding="utf-8")
            test.to_csv(test_path, sep=",", index=False, encoding="utf-8")
            logger.info(
                "dataset splitted to train and test and saved in the: data/processed directory")
        except Exception as e:
            raise CustomException(e, sys)

    def feature_engineering(self):
        try:
            # load the dataset
            df = pd.read_csv(self.config.data_load.dataset_path)
            logger.info(f"dataset loaded successfully!{df.head()}")

            # remove the id column
            df = df.drop(['id'], axis=1)
            logger.info("'id' column removed successfully!")

            # remove other elements from gender column
            i = df[df.gender == 'Other'].index
            df = df.drop(i)
            logger.info(
                "'other' feature from gender column removed successfully!")

            # fill null values with median (we select median cause of outliers)
            df.fillna(df.bmi.median(), inplace=True)
            df.isnull().sum()
            logger.info("Missing values handled")

            # encoding categorical features
            df['gender'].replace(
                to_replace={'Female': 0, 'Male': 1}, inplace=True)
            df['ever_married'].replace(
                to_replace={'No': 0, 'Yes': 1}, inplace=True)
            df['Residence_type'].replace(
                to_replace={'Rural': 0, 'Urban': 1}, inplace=True)

            encoder = LabelEncoder()
            df['work_type'] = encoder.fit_transform(df['work_type'])
            df['smoking_status'] = encoder.fit_transform(df['smoking_status'])

            logger.info(
                "Transformed categorical variables into numerical representations")

            # handling imbalance data
            os = RandomOverSampler()
            X, y = os.fit_resample(df.drop(['stroke'], axis=1), df.stroke)
            df = X
            df['stroke'] = y

            logger.info(
                f"Imbalance data handled:\n {df.stroke.value_counts()}")

            # calling a function that handle outliers
            self.handle_outliers(df)
            logger.info(f"Outliers handled: {df.bmi.max(), df.bmi.min()}")

            print(df.head())

            # calling a function split_save_train_test
            self.split_save_train_test(df)

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=Path("params.yaml"))
    parsed_args = args.parse_args()
    data_preprocess = Data_Preprocessing(params_file=parsed_args.config)
    # data_preprocess.display_dataset()
    data_preprocess.feature_engineering()
