CMPE 131
READ ME FILE 
Team: Lennie Gonsalves, Ben Gonzalez, Dominic Gutierrez, Alireza Parvar

To start up the application:
1) Clone the CMPE-131 repository into a directory on ubuntu, with
    (git clone https://github.com/Alireza-Mahinparvar/BookMe)
2) pip install flask, flask_sqlalchemy, flask_wtf, wtforms.validators, 
                      wheel, email_validator, datetime, calendar
3) Go into the Calendar_app folder, with (cd Calendar_app)
4) Run the "run.py" file

If the website is not allowing you to login or create an account, try recreating the app.db file.

To recreate app.db:
>>> from app import db 
>>> from app.models import User, Post

>>> db.create_all()     # creates database

>>> u = User(username='tra', email='tra@example.com’)

>>> db.session.add(u)   # similar to staging in git
>>> db.session.commit() # writes to database

To book a meeting: 
Click on Book Meeting >> Click on a username >> Choose a day from the calendar >> Fill out meeting form >> Submit

