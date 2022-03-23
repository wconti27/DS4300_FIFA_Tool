# DS4300_FIFA_Tool

## Steps to run

### 1: Run the following command to clone repo into folder of your choosing.


    git clone https://github.com/wconti27/DS4300_FIFA_Tool.git

### 2: Create a virtual environment (.venv) to handle project dependencies and activate it. 

    python -m venv .venv

#### To activate it, command for mac:
    source .venv/bin/activate

#### To activate it, command for windows:
    .venv\Scripts\activate.bat

NOTE: If not already install, use pip to install package venv through terminal:

    python -m pip install venv

### 3: Install project dependencies

    pip install -f requirements.txt

### 4: Start mongodb and run import_data script:
    mongod
    python import_data.py

### 5: Start Flask app (and add FLASK env variables to system env variables)
    set FLASK_APP=app
    set FLASK_ENV=development
    flask run
