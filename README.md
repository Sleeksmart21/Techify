# Techify
## A Blog for Tech Stories, where Techies share their experiences in their Tech journey, their inspirations and aspirations.

### Requirements
Python3 Flask virtual Envrionment

## Getting Started
### To succesfully install and run this app, do the following:
Install a virtual environment - pip3 install virtualenv<br>
Create a virtual environment - virtualenv env<br>
Activate virtual environment - source env/bin/activate<br>
Install Flask - pip3 install flask<br>
Install sqlalchemy - pip3 install flask-sqlalchemy<br>
#### Note: The version of flask and flask-sqlalchemy for this project is in the requirements.txt file<br>

Create the database - on the terminal, run the following commands:<br>
from app import app<br>
from app import db, User<br>
with app.app_context():<br>
  db.create_all()<br>
  
Line 17 is the last command but before typing, press the tab key and after typing, press the enter key twice.


