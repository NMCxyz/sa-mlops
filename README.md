# End-To-End-MLOps-Project


```bash
## MLOps Lifecycle:

    1. Problem Definition and Requirement Gathering
    2. EDA
    3. Feature Engineering
    4. Feature Selection
    5. Model Creation
    6. Model Hyper-parameter Tunning
    7. Model Deployment
    8. Retraining Approaches
```

## Steps:

1. Git clone the repository and Define template of the project

```bash
touch template.py
python3 template.py
```

2. define setup.py scripts (**The setup.py** is a module used to build and distribute Python packages. It typically contains information about the package)


3. Create environment and install dependencies

```bash
conda create -n mlops-env python=3.9 -y
conda activate mlops-env
pip install -r requirements.txt
```

4. define custom exception and define logger (**The Logging** is a means of tracking events that happen when some software runs)

5. define utils (**The utils.py** makes it easy to execute common tasks in Python scripts)

6. **Data Ingesstion Section**
 * constants added
 * params.yaml defined
 * 01_data_ingeston.ipynb created
 * stage_01_data_ingeston.py created
 * data downloaded

7. **DVC Section**
 * run dvc init
 * define data_ingeston stage in dvc.yaml
 * run dvc repro

8. **EDA**
 * load the dataset
 * statistical checking
 * checking number of unique values for each columns
 * check data type
 * check duplicate values
 * check null values
 * check balance of the dataset
 * check outliers
 * visualization
 * checking correlation

9. **Data Preprocessing Section**
* params.yaml defined
* 02_data_preprocessing.ipynb added
* stage_02_data_preprocessing.py created
* data_preprocessing stage added to dvc.yaml

10. **Model Training Section**
* define params.yaml
* created 03_model_training.ipynb
* mlflow added to the project
```bash
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./artifacts \
    --host 0.0.0.0 -p 1234
----------------------------------------------------------------
mlflow server --backend-store-uri sqlite:///mlflow.db  --host 0.0.0.0 -p 1234 --default-artifact-root ./artifacts


```
* stage_03_training_and_evaluation.py created
* model_train_evaluation stage added to dvc pipeline


11. **Log Prediction Model**
* params.yaml defined
* 04_log_production_model.ipynb created
* model_regiseter_name added to stage_03_training_and_evaluation.py
* stage_04_log_production_model.py created
* logg_production_model stage added to dvc
* model with best accuracy loaded in mlflow and saved


12. **Flask App**
 * add the required html and css to the project
 * define app.py
 * run the app

13. **Docker And CICD**
* define the docker file
* create .github/workflows/docker_cicd.yaml and define it
* DOCKER_USERNAME=?
* DOCKER_PASSWORD=?
* push the changes


**************************************************************************************************************************

14. **AWS Section**

**Note:** we will deploy AWS-CICD using Github-Actions

### 1. Login to AWS console
### 2. Create IAM user for deployment and download the stroke_predictor_accessKeys
```bash
#with specific access

1. ECR: Elastic Container registry to save your docker image in aws
2. EC2 access : It is virtual machine


#Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

#Policy for IAM:

1. AmazonEC2ContainerRegistryFullAccess
2. AmazonEC2FullAccess
```

### 3. Create ECR repo to store/save docker image
```bash
- Save the URI: 060145207853.dkr.ecr.ap-south-1.amazonaws.com/stroke_predictor
```

### 4. Create EC2 machine (Ubuntu)
### 5. Open EC2 and Install docker in EC2 Machine:
```bash
#optinal

sudo apt-get update

sudo apt-get upgrade -y

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```
### 6. Configure EC2 as self-hosted runner:
```bash
setting-->actions-->runner-->new self hosted runner--> choose os--> copy each command and run it on EC2 Instance Connect
```
### 7. Setup github secrets:
```bash
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = ap-south-1

AWS_ECR_LOGIN_URI = demo>>  060145207853.dkr.ecr.ap-south-1.amazonaws.com

ECR_REPOSITORY_NAME = stroke_predictor
```
******************************************************************************************************
