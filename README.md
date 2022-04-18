# 3AK Pharma - An Integrated Cloud Based Heathcare Solution

## Installation steps 

### Dependencies to be installed on Linux system

```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo pip install virtualenv
sudo apt-get install libmysqlclient-dev
```

### Create virtual environment and install the required dependencies in virtual environment

```bash
mkdir 3AKPharma
cd 3AKPharma
source env/bin/activate
git clone https://github.com/ketanmb69/3AKPharma.git
pip install --upgrade setuptools
cd 3AK
pip install -r requirements.txt
```

## Run the application from scratch
```bash
find . -name migrations | xargs rm -rf 
rm -rf db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py runserver
```
## Steps to Deploy on Elastic Beanstalk

- Make sure the file named **Procfile** is present in the environment - ```web: gunicorn 3AK.wsgi```
- make sure the directory named **.ebextensions** is present and **django.config** has below details
  - ```python
    option_settings:
      aws:elasticbeanstalk:container:python:
        WSGIPath: 3AK/wsgi.py
    ```
- Create Sample Elastic Beanstalk **Worker** environment.
  - Go to the additional configuration settings and update as **Highly Available application** (It will spawn the mutliple instances.)

- Create a Code Pipeline and choose the source control as per convinience.
  - Skip the build stage.
  - Select the Elastic Beanstalk as a deployment provider.
  - Specify the Elastic Beanstalk application name, and the Environment name as provided while creating the Beanstalk sample application.
  - Create a pipeline.
  - After successful deployment,, go to the Elastic beanstalk environment and open the application link. it will be a **Load Balancer** link.
