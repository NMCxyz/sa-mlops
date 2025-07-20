from src.utils.common import read_yaml
from src.constants import PARAMS_FILE_PATH
from src.exception import CustomException
from src import logger

import pandas as pd
import matplotlib.pyplot as plt


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import (accuracy_score,
                             f1_score,
                             confusion_matrix,
                             ConfusionMatrixDisplay,
                             auc,
                             roc_curve,
                             RocCurveDisplay)
import mlflow
from pathlib import Path
import argparse
import sys


class Model_train:

    def __init__(self, params_file=PARAMS_FILE_PATH):
        self.config = read_yaml(params_file)

    def prepare_train_test(self):
        try:
            train_path = self.config.split_data.train_path
            test_path = self.config.split_data.test_path
            df_train = pd.read_csv(train_path)
            df_test = pd.read_csv(test_path)

            X_train = df_train.drop(['stroke'], axis=1)
            y_train = df_train['stroke']
            X_test = df_test.drop(['stroke'], axis=1)
            y_test = df_test['stroke']

            return (X_train, y_train, X_test, y_test)
        except Exception as e:
            raise CustomException(e, sys)

    # fun to create confusion matrix
    def create_confusion_matrix_plot(self, clf, y_test, predictions):

        cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                      display_labels=clf.classes_)
        disp.plot()
        plt.savefig('confusion_matrix.png')

    # fun to create roc_curve

    def create_roc_auc_plot(self, y_test, predictions):

        fpr, tpr, thresholds = roc_curve(y_test, predictions)
        roc_auc = auc(fpr, tpr)
        disp = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc,
                               estimator_name='example estimator')
        disp.plot()
        plt.savefig('roc_auc_curve.png')

    def Mlflow_Model_Hyperparametrs(self):
        try:
            X_train, y_train, X_test, y_test = self.prepare_train_test()
            logger.info(
                "successfully loaded: X_train, y_train, X_test, y_test")

            remote_server_uri = self.config.mlflow_config.remote_server_uri
            experiment_name = self.config.mlflow_config.experiment_name
            run_name = self.config.mlflow_config.run_name

            # mlflow.set_tracking_uri(remote_server_uri) # error...
            # mlflow.set_tracking_uri("http://localhost:1234")
            mlflow.set_tracking_uri("http://localhost:5000")

            mlflow.set_experiment(experiment_name)

            with mlflow.start_run(run_name=run_name) as mlops_run:
                # Define a grid of hyperparameters
                grid = {"n_estimators": [10, 100, 200, 500],
                        'criterion': ['gini', 'entropy', 'log_loss'],
                        "max_depth": [None, 5, 10, 20, 30],
                        "min_samples_split": [2, 4, 6],
                        "min_samples_leaf": [1, 2, 4]
                        }
                # run a randomized search cv
                rs_RFC = RandomizedSearchCV(estimator=RandomForestClassifier(),
                                            param_distributions=grid,
                                            n_iter=5,
                                            verbose=True)

                rs_RFC.fit(X_train, y_train)
                logger.info("Randomized search cv finished.")

                # loging the best params
                run_params = rs_RFC.best_params_
                for param in run_params:
                    mlflow.log_param(param, run_params[param])
                logger.info("log params: %s", run_params)

                # train RandomForest with best params
                model = RandomForestClassifier(**run_params)
                model.fit(X_train, y_train)
                logger.info("Training RandomForest with best params")

                y_pred = model.predict(X_test)
                acu = accuracy_score(y_test, y_pred)
                f1score = f1_score(y_test, y_pred)

                # loging accuracy and f1_score
                mlflow.log_metric("acu", acu)
                mlflow.log_metric("f1_score", f1score)
                logger.info("logging accuracy and f1_score")

                # confusion matrix
                self.create_confusion_matrix_plot(model, y_test, y_pred)
                mlflow.log_artifact('confusion_matrix.png',
                                    'confusion_materix')
                logger.info("confusion_matrix.png added")

                # roc curve plot
                self.create_roc_auc_plot(y_test, y_pred)
                mlflow.log_artifact('roc_auc_curve.png', "roc_auc_plot")
                logger.info("roc_auc_curve.png added")

                # Save the model using mlflow.<framework>.log_model()
                mlflow.sklearn.log_model(sk_model=model,
                                         artifact_path='models_mlflow',
                                         registered_model_name=self.config.mlflow_config.registered_model_name)
                logger.info("Model saved")
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=Path("params.yaml"))
    parsed_args = args.parse_args()
    model_training = Model_train(params_file=parsed_args.config)
    model_training .Mlflow_Model_Hyperparametrs()
