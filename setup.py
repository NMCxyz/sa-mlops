import setuptools


__version__ = "0.0.1"

SRC_REPO = "End-To-End-MLOps-Project"
AUTHOR_USER_NAME = "FraidoonOmarzai"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    description="Implementation of mlops projects",
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),


)