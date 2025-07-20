import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

dirs = [
    os.path.join("data", "raw"), ## <- Store the raw data in a directory
    os.path.join("data", "processed"), ## <- store the prepared-data in a directory
    os.path.join("src", "constants"),  ## <- define our constants variables
    os.path.join("src", "utils"),  ## <- define our common methods
    os.path.join("src", "pipeline"),  ## <- define our pipeline
    "notebooks",
    "saved_models",
    "webapp"
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    # To get Git to recognize an empty directory, the unwritten rule is to put a file named .gitkeep in it
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        logging.info(f"Creating directory:{dir_}")
        pass


files = [
    "dvc.yaml",
    "params.yaml",
    "Dockerfile",
    "setup.py",
    "app.py",
    "requirements.txt",
    os.path.join("src", "__init__.py")
]

for file_ in files:
    with open(file_, "w") as f:
        logging.info(f"Creating file: {file_}")    
        pass