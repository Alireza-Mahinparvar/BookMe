CMPE 131


To start up the application:
1) Clone the CMPE-131 repository into a directory on ubuntu, with
    (git clone https://github.com/cmpe131-spring2020/CMPE-131)
2) Go into the Calendar_app folder, with (cd Calendar_app)
3) Run the "run.py" file

To recreate app.db:
>>> from app import db 
>>> from app.models import User, Post

>>> db.create_all()     # creates database

>>> u = User(username='tra', email='tra@example.com’)

>>> db.session.add(u)   # similar to staging in git
>>> db.session.commit() # writes to database
