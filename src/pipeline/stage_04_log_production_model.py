from src.utils.common import read_yaml
from src.constants import PARAMS_FILE_PATH
from src import logger

import mlflow
from mlflow.tracking import MlflowClient
import joblib

import argparse
from pathlib import Path


class Log_Production_Model:

    def __init__(self, params_file=PARAMS_FILE_PATH):
        self.config = read_yaml(params_file)

    def log_pro_model(self):
        config = self.config

        model_name = config.mlflow_config.registered_model_name

        remote_server_uri = config.mlflow_config.remote_server_uri
        mlflow.set_tracking_uri(remote_server_uri)
        # mlflow.set_tracking_uri("http://localhost:5000")
        

        # runs = mlflow.search_runs(experiment_ids=[0, 1, 2])
        runs = mlflow.search_runs(experiment_ids=config.mlflow_config.experiment_id) # in params.yaml
        highest = runs["metrics.acu"].sort_values(
            ascending=False, ignore_index=True)[0]
        highest_run_id = runs[runs["metrics.acu"] == highest]["run_id"]
        highest_run_id = highest_run_id.reset_index(drop=True)[0]
        logger.info(
            f"higest_acu: {highest} and highest run id: {highest_run_id}")

        client = MlflowClient()
        for mv in client.search_model_versions(f"name='{model_name}'"):
            mv = dict(mv)

            if mv["run_id"] == highest_run_id:
                current_version = mv["version"]
                logged_model = mv["source"]
                client.transition_model_version_stage(
                    name=model_name,
                    version=current_version,
                    stage="Production"
                )
            else:
                current_version = mv["version"]
                client.transition_model_version_stage(
                    name=model_name,
                    version=current_version,
                    stage="Staging"
                )
        logger.info("Staging section done")

        loaded_model = mlflow.pyfunc.load_model(logged_model)

        model_path = config.webapp_model_dir
        joblib.dump(loaded_model, model_path)

        logger.info("Loaded model successfully, Model_path: {model_path}".format(
            model_path=model_path))


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=Path("params.yaml"))
    parsed_args = args.parse_args()
    log_model = Log_Production_Model(params_file=parsed_args.config)
    log_model.log_pro_model()