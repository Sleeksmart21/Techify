# Techify
## A Blog for Tech Stories, where Techies share their experiences in their Tech journey, their inspirations and aspirations.

### Requirements
Python3 Flask virtual Envrionment

## Getting Started
### To succesfully install and run this app, do the following:
Install a virtual environment - pip3 install virtualenv
Create a virtual environment - virtualenv env
Activate virtual environment - source env/bin/activate
Install Flask - pip3 install flask
Install sqlalchemy - pip3 install flask-sqlalchemy
#### Note: The version of flask and flask-sqlalchemy for this project is in the requirements.txt file

Create the database - on the terminal, run the following commands:
from app import app
from app import db, User
with app.app_context():
  db.create_all()
  
Line 17 is the last command but before typing, press the tab key and after typing, press the enter key twice.


